#!/usr/bin/env python
"""
Script to set up test data for Stationery World Uganda
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stationaryworld.settings')
django.setup()

from main.models import Product, PaymentMethod

def create_test_products():
    """Create test products for testing"""
    
    products_data = [
        {
            'name': 'A4 Writing Pad',
            'description': 'High-quality A4 writing pad for all your writing needs. Perfect for notes, letters, and official documents.',
            'price': 15000.00,
            'category': 'stationery',
        },
        {
            'name': 'Ballpoint Pens (Pack of 10)',
            'description': 'Smooth writing ballpoint pens in blue ink. Ideal for office and school use.',
            'price': 25000.00,
            'category': 'stationery',
        },
        {
            'name': 'USB Flash Drive 32GB',
            'description': 'High-speed USB flash drive for data storage. Compatible with all devices.',
            'price': 45000.00,
            'category': 'electronics',
        },
        {
            'name': 'Desktop Organizer',
            'description': 'Keep your workspace tidy with this premium desktop organizer.',
            'price': 35000.00,
            'category': 'stationery',
        },
        {
            'name': 'Graphic Design Services',
            'description': 'Professional graphic design services for all your branding needs.',
            'price': 150000.00,
            'category': 'design',
        },
        {
            'name': 'Digital Printing Services',
            'description': 'High-quality digital printing for business cards, flyers, and documents.',
            'price': 75000.00,
            'category': 'printing',
        }
    ]
    
    print("Creating test products...")
    
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        
        if created:
            print(f"[CREATED] {product.name} - UGX {product.price}")
        else:
            print(f"[EXISTS] {product.name} - UGX {product.price}")
    
    print(f"\nTotal products: {Product.objects.count()}")
    return Product.objects.all()

def verify_payment_method():
    """Verify cash on delivery payment method exists"""
    
    payment_method = PaymentMethod.objects.filter(provider='cash', is_active=True).first()
    
    if payment_method:
        print(f"[VERIFIED] Payment Method: {payment_method.name} - {payment_method.provider}")
        return True
    else:
        print("[ERROR] No cash on delivery payment method found!")
        return False

def main():
    """Main setup function"""
    
    print("=== Stationery World Uganda - Test Data Setup ===\n")
    
    # Verify payment method
    if not verify_payment_method():
        print("Please run 'python init_payment_methods.py' first")
        return
    
    # Create test products
    products = create_test_products()
    
    print(f"\n=== Setup Complete ===")
    print(f"✅ {products.count()} products ready for testing")
    print(f"✅ Cash on delivery payment method configured")
    print(f"✅ Server running at: http://127.0.0.1:8000/")
    print(f"\n🔗 Test the application:")
    print(f"   - Homepage: http://127.0.0.1:8000/")
    print(f"   - Products: http://127.0.0.1:8000/products/")
    print(f"   - Contact: http://127.0.0.1:8000/contact/")

if __name__ == '__main__':
    main()