#!/usr/bin/env python
"""
Script to initialize payment methods for Stationery World Uganda
Run this script after migrating the database to populate payment methods
"""

import os
import sys
import django
from decimal import Decimal

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stationaryworld.settings')
django.setup()

from main.models import PaymentMethod

def create_payment_methods():
    """Create default payment methods - cash on delivery only"""
    
    # Clear existing payment methods first
    PaymentMethod.objects.all().delete()
    
    # Only create cash on delivery payment method
    payment_methods = [
        {
            'name': 'Cash on Delivery',
            'provider': 'cash',
            'is_active': True,
            'processing_fee': Decimal('0.00')
        }
    ]
    
    print("Creating cash on delivery payment method...")
    
    for method_data in payment_methods:
        method, created = PaymentMethod.objects.get_or_create(
            provider=method_data['provider'],
            defaults=method_data
        )
        
        if created:
            print(f"[CREATED] {method.name}")
        else:
            print(f"[EXISTS] {method.name}")
    
    print(f"\nTotal payment methods: {PaymentMethod.objects.count()}")
    print("Payment methods initialization complete!")

if __name__ == '__main__':
    create_payment_methods()