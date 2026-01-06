from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, Payment, PaymentMethod, PaymentCallback, WebsiteContent, ContactInfo, ServiceInfo, ServiceImage, ServiceInfoLegacy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json

def home(request):
    products = Product.objects.order_by('-priority', 'name')
    return render(request, 'main/home.html', {'products': products})

def products(request):
    products = Product.objects.order_by('-priority', 'name')
    return render(request, 'main/products.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'main/product_detail.html', {'product': product})

def services(request):
    """Show services with images"""
    # Get active services with their images
    services = ServiceInfo.objects.filter(is_active=True).prefetch_related('images')
    
    # If no services exist, create default ones using legacy data
    if not services.exists():
        # Create default services using legacy data
        legacy_service = ServiceInfoLegacy.objects.first()
        if legacy_service:
            default_services = [
                {
                    'name': 'graphic_design',
                    'title': 'Graphic Design',
                    'description': legacy_service.graphic_design_description,
                    'images': ['image1.png', 'image2.png', 'image3.png']  # Default images
                },
                {
                    'name': 'printing',
                    'title': 'Printing & Photocopying',
                    'description': legacy_service.printing_description,
                    'images': ['Digital-Printing-Services.jpg', 'image5.png', 'image6.png']
                },
                {
                    'name': 'electronics',
                    'title': 'Electronics',
                    'description': legacy_service.electronics_description,
                    'images': ['image8.png', 'image9.png', 'image10.png']
                },
                {
                    'name': 'stationery',
                    'title': 'Stationery Supply',
                    'description': legacy_service.stationery_description,
                    'images': ['desktop organiser.jpg', 'image11.jpg', 'image12.png']
                }
            ]
            
            # Create ServiceInfo objects and associate images
            for i, service_data in enumerate(default_services):
                service = ServiceInfo.objects.create(
                    name=service_data['name'],
                    title=service_data['title'],
                    description=service_data['description'],
                    display_order=i
                )
                
                # Create service images
                for j, image_name in enumerate(service_data['images']):
                    ServiceImage.objects.create(
                        service=service,
                        image=f'products/{image_name}',
                        display_order=j
                    )
            
            # Get the newly created services
            services = ServiceInfo.objects.filter(is_active=True).prefetch_related('images')
    
    return render(request, 'main/services.html', {'services': services})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        try:
            # Compose email subject and message
            email_subject = f'New Customer Inquiry from {name}'
            email_body = f'''
You have received a new customer inquiry from your website:

Customer Details:
- Name: {name}
- Email: {email}
- Phone: {phone}

Message:
{message}

Please respond to this customer promptly.

Best regards,
Stationery World Uganda Website
            '''
            
            # Send email to Stationery World
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.STATIONERY_WORLD_EMAIL],
                fail_silently=False,
            )
            
            messages.success(request, 'Thank you for contacting us! We have received your message and will get back to you soon.')
            
        except Exception as e:
            # Log the error (in production, use proper logging)
            print(f"Email sending failed: {str(e)}")
            messages.error(request, 'Sorry, there was an error sending your message. Please try again or contact us directly.')
        
        return render(request, 'main/contact.html')
    
    return render(request, 'main/contact.html')

def order(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')
            quantity = request.POST.get('quantity', 1)
            name = request.POST.get('customer_name')
            phone = request.POST.get('customer_phone')
            
            # Validate required fields
            if not all([product_id, name, phone]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('products')
            
            # Get the product
            product = Product.objects.get(id=product_id)
            
            # Create the order
            order = Order.objects.create(
                product=product,
                quantity=int(quantity) if quantity else 1,
                customer_name=name,
                customer_phone=phone
            )
            
            # Redirect to cash on delivery confirmation page
            return redirect('create_payment', order_id=order.id)
            
        except Product.DoesNotExist:
            messages.error(request, 'Product not found. Please try again.')
            return redirect('products')
        except ValueError:
            messages.error(request, 'Invalid quantity. Please enter a valid number.')
            return redirect('products')
        except Exception as e:
            messages.error(request, 'An error occurred while processing your order. Please try again.')
            return redirect('products')
    else:
        # If not POST, redirect to products page
        return redirect('products')


def create_payment(request, order_id):
    """Create a payment for an order - cash on delivery only"""
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        try:
            # For cash on delivery, we don't need to select payment method
            # Just get the single available payment method (cash on delivery)
            payment_method = get_object_or_404(PaymentMethod, provider='cash', is_active=True)
            
            # Calculate total amount (no processing fee for cash on delivery)
            total_amount = float(order.product.price) * order.quantity
            final_amount = total_amount
            
            # Create payment record
            payment = Payment.objects.create(
                order=order,
                payment_method=payment_method,
                amount=final_amount,
                status='processing'  # Start as processing since it's COD
            )
            
            # Redirect to success page (no payment processing needed for COD)
            messages.success(request, f'Order confirmed for {order.product.name}! You will pay {order.product.price * order.quantity} UGX upon delivery.')
            return redirect('payment_success', payment_id=payment.id)
            
        except Exception as e:
            messages.error(request, 'Error creating order. Please try again.')
            return redirect('products')
    
    # For cash on delivery, we skip the payment method selection page
    # and directly create a payment record
    payment_method = get_object_or_404(PaymentMethod, provider='cash', is_active=True)
    
    total_amount = float(order.product.price) * order.quantity
    
    return render(request, 'main/cash_on_delivery_confirmation.html', {
        'order': order,
        'total_amount': total_amount,
        'payment_method': payment_method
    })


def process_payment(request, payment_id):
    """Process payment - simplified for cash on delivery only"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    # For cash on delivery, we don't need a separate processing page
    # The payment is automatically in 'processing' status
    return redirect('payment_success', payment_id=payment.id)





@csrf_exempt
@require_http_methods(["POST"])
def payment_callback(request):
    """Handle payment callbacks from providers"""
    try:
        data = json.loads(request.body)
        
        # In a real implementation, verify the callback authenticity
        transaction_id = data.get('transaction_id')
        
        if transaction_id:
            payment = Payment.objects.get(transaction_id=transaction_id)
            
            # Create callback record
            PaymentCallback.objects.create(
                payment=payment,
                provider=data.get('provider', 'unknown'),
                callback_data=data
            )
            
            # Update payment status based on callback
            if data.get('status') == 'success':
                payment.mark_completed(
                    provider_transaction_id=data.get('provider_transaction_id'),
                    provider_response=data
                )
            elif data.get('status') == 'failed':
                payment.mark_failed(provider_response=data)
            
            return JsonResponse({'status': 'received'})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid callback'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def payment_success(request, payment_id):
    """Show payment success page"""
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'main/payment_success.html', {'payment': payment})


def payment_pending(request, payment_id):
    """Show payment pending page"""
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'main/payment_pending.html', {'payment': payment})


# Admin Views
def admin_login(request):
    """Admin login view"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username, password, or insufficient permissions.')
    
    return render(request, 'admin/login.html')


@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    # Get or create content instances
    content, created = WebsiteContent.objects.get_or_create(pk=1)
    contact, created = ContactInfo.objects.get_or_create(pk=1)
    services, created = ServiceInfoLegacy.objects.get_or_create(pk=1)
    
    # Get recent orders
    recent_orders = Order.objects.select_related('product', 'payment').order_by('-date_ordered')[:10]
    
    return render(request, 'admin/dashboard.html', {
        'content': content,
        'contact': contact,
        'services': services,
        'recent_orders': recent_orders
    })


@login_required
def admin_update_content(request):
    """Update website content"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    if request.method == 'POST':
        content, created = WebsiteContent.objects.get_or_create(pk=1)
        content.welcome_title = request.POST.get('welcome_title', content.welcome_title)
        content.welcome_description = request.POST.get('welcome_description', content.welcome_description)
        content.company_description = request.POST.get('company_description', content.company_description)
        content.save()
        messages.success(request, 'Website content updated successfully!')
    
    return redirect('admin_dashboard')


@login_required
def admin_update_contact(request):
    """Update contact information"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    if request.method == 'POST':
        contact, created = ContactInfo.objects.get_or_create(pk=1)
        contact.address = request.POST.get('address', contact.address)
        contact.phone = request.POST.get('phone', contact.phone)
        contact.email = request.POST.get('email', contact.email)
        contact.business_hours = request.POST.get('business_hours', contact.business_hours)
        contact.save()
        messages.success(request, 'Contact information updated successfully!')
    
    return redirect('admin_dashboard')


@login_required
def admin_update_services(request):
    """Update services information"""
    if not request.user.is_staff:
        return redirect('admin_login')

    if request.method == 'POST':
        services, created = ServiceInfoLegacy.objects.get_or_create(pk=1)
        services.graphic_design_description = request.POST.get('graphic_design_description', services.graphic_design_description)
        services.printing_description = request.POST.get('printing_description', services.printing_description)
        services.electronics_description = request.POST.get('electronics_description', services.electronics_description)
        services.stationery_description = request.POST.get('stationery_description', services.stationery_description)
        services.save()
        messages.success(request, 'Services information updated successfully!')

    return redirect('admin_dashboard')


@login_required
def admin_logout(request):
    """Admin logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
