from django.contrib import admin
from .models import Product, Order, ProductImage, Payment, PaymentMethod, WebsiteContent, ContactInfo, ServiceInfo

# Customize Django Admin Site
admin.site.site_header = "Stationery World Uganda - Administration"
admin.site.site_title = "Stationery World Uganda Admin"
admin.site.index_title = "Welcome to Stationery World Uganda Dashboard"

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'price', 'category', 'priority')
    list_display_links = ('category',)
    list_editable = ('name', 'price', 'priority')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('-priority', 'name')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'product', 'quantity', 'date_ordered', 'fulfilled')
    list_filter = ('fulfilled', 'date_ordered')
    search_fields = ('customer_name', 'product__name')
    ordering = ('-date_ordered',)

# Register all models with custom admin classes
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(PaymentMethod)
admin.site.register(WebsiteContent)
admin.site.register(ContactInfo)
admin.site.register(ServiceInfo)
