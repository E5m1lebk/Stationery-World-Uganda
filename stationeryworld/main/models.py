from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

def generate_transaction_id():
    return str(uuid.uuid4())

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=[
        ('stationery', 'Stationery'),
        ('electronics', 'Electronics'),
        ('design', 'Design'),
        ('printing', 'Printing'),
    ])
    priority = models.IntegerField(default=0, help_text='Higher priority products appear first')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.product.name} image"

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20, null=True, blank=True) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_ordered = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer_name} - {self.product.name}"


class PaymentMethod(models.Model):
    """Available payment methods - now only cash on delivery"""
    name = models.CharField(max_length=50, default='Cash on Delivery')
    provider = models.CharField(max_length=50, choices=[
        ('cash', 'Cash on Delivery'),
    ], default='cash')
    is_active = models.BooleanField(default=True)
    processing_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.name} ({self.get_provider_display()})"


class Payment(models.Model):
    """Payment records"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, default=generate_transaction_id)
    provider_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    provider_response = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.order}"
    
    def mark_completed(self, provider_transaction_id=None, provider_response=None):
        self.status = 'completed'
        self.provider_transaction_id = provider_transaction_id
        self.provider_response = provider_response
        self.processed_at = timezone.now()
        self.save()
    
    def mark_failed(self, provider_response=None):
        self.status = 'failed'
        self.provider_response = provider_response
        self.save()


class PaymentCallback(models.Model):
    """Store payment provider callbacks for debugging"""
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='callbacks')
    provider = models.CharField(max_length=50)
    callback_data = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Callback for {self.payment.transaction_id} from {self.provider}"


class WebsiteContent(models.Model):
    """Store website content that can be edited by admin"""
    welcome_title = models.CharField(max_length=200, default='Welcome to Stationery World Uganda')
    welcome_description = models.TextField(default='Your trusted partner in Stationery, Electronics, Phone Accessories, Graphic Designing & Printing')
    company_description = models.TextField(default='We provide quality stationery, electronics, and printing services to individuals and businesses across Uganda.')
    
    def __str__(self):
        return "Website Content Settings"


class ContactInfo(models.Model):
    """Store contact information"""
    address = models.CharField(max_length=300, default='Nabweru near playground, Wakiso, Uganda')
    phone = models.CharField(max_length=100, default='0200 901 914, +256 783 238 522')
    email = models.EmailField(default='clericdesigns@gmail.com')
    business_hours = models.CharField(max_length=200, default='Monday - Friday: 07:00 AM - 10:00 PM, Saturday & Sunday: 8:00 AM - 10:00 PM')
    
    def __str__(self):
        return "Contact Information"


class ServiceInfo(models.Model):
    """Store service information"""
    SERVICE_TYPES = [
        ('graphic_design', 'Graphic Design'),
        ('printing', 'Printing & Photocopying'),
        ('electronics', 'Electronics'),
        ('stationery', 'Stationery Supply'),
    ]
    
    name = models.CharField(max_length=100, choices=SERVICE_TYPES, default='graphic_design')
    title = models.CharField(max_length=200, default='Service Title')
    description = models.TextField(default='Service description')
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        ordering = ['display_order', 'name']

class ServiceImage(models.Model):
    """Store multiple images for each service"""
    service = models.ForeignKey(ServiceInfo, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='services/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    display_order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.service.get_name_display()} image"
    
    class Meta:
        ordering = ['display_order', 'id']

# Keep the old ServiceInfo for backward compatibility
class ServiceInfoLegacy(models.Model):
    """Store service information (legacy)"""
    graphic_design_description = models.TextField(default='Professional graphic design services for all your branding and marketing needs.')
    printing_description = models.TextField(default='High-quality printing services for all your documents and marketing materials.')
    electronics_description = models.TextField(default='Quality electronics and accessories for all your technology needs.')
    stationery_description = models.TextField(default='Complete stationery solutions for offices, schools, and personal use.')
    
    def __str__(self):
        return "Service Information"
