# Stationery World Uganda - Fonts & Payment Integration

## Overview
This project has been enhanced with web fonts support and a comprehensive payment integration system for the Stationery World Uganda e-commerce platform.

## ✅ Completed Features

### 1. Fonts Integration
**Location**: `stationeryworld/main/static/fonts/`

- **Font Folders Created**:
  - `nexa/` - Nexa font family
  - `poppins/` - Poppins font family  
  - `montserrat/` - Montserrat font family

- **Files Created**:
  - `fonts.css` - Complete font-face declarations for all font weights
  - `README.md` - Instructions for adding fonts to the project
  - Font folders ready to receive font files (.woff2, .woff, .ttf, .otf)

- **Base Template Updated**:
  - Added Font Awesome icons for payment templates
  - Integrated fonts.css into base.html
  - Added Google Fonts fallbacks

### 2. Payment Integration System
**Database Models**:
- `PaymentMethod` - Available payment providers
- `Payment` - Individual payment transactions
- `PaymentCallback` - Payment provider callback logging

**Supported Payment Methods**:
- MTN Mobile Money
- Airtel Money  
- Credit/Debit Card
- Bank Transfer
- Cash on Delivery

**URL Routes Added**:
- `/payment/create/<order_id>/` - Create payment for order
- `/payment/process/<payment_id>/` - Process payment
- `/payment/success/<payment_id>/` - Payment success page
- `/payment/pending/<payment_id>/` - Payment pending page
- `/payment/callback/` - Payment provider callbacks

**Templates Created**:
- `create_payment.html` - Payment method selection
- `process_payment.html` - Payment processing interface
- `payment_success.html` - Success confirmation
- `payment_pending.html` - Pending status page

### 3. Payment Processing Features
- **Transaction IDs**: Unique UUID-based transaction tracking
- **Provider Integration**: Framework ready for real payment provider APIs
- **Status Tracking**: Complete payment lifecycle management
- **Callback Handling**: Webhook support for payment notifications
- **Processing Fees**: Configurable fees per payment method

## 🚀 How to Use

### Adding Fonts
1. Download font files (preferably .woff2 format)
2. Place them in the appropriate folder:
   - `main/static/fonts/nexa/` for Nexa fonts
   - `main/static/fonts/poppins/` for Poppins fonts
   - `main/static/fonts/montserrat/` for Montserrat fonts
3. The `fonts.css` file already contains the font-face declarations
4. Use the fonts in your CSS: `font-family: 'Poppins', sans-serif;`

### Creating Payments
1. An order is created through the existing order system
2. Navigate to `/payment/create/<order_id>/` to select payment method
3. Complete payment through the appropriate provider interface
4. Track payment status through the success/pending pages

### Payment Provider Integration
The system is designed to be extended with real payment provider APIs. Currently includes:

- **MTN Mobile Money**: Framework for integration
- **Airtel Money**: Framework for integration  
- **Card Payments**: Ready for Stripe/Paystack integration
- **Bank Transfer**: Manual confirmation process
- **Cash on Delivery**: No online payment required

## 📁 File Structure

```
stationeryworld/
├── main/
│   ├── static/
│   │   ├── fonts/
│   │   │   ├── fonts.css          # Font declarations
│   │   │   ├── README.md          # Font usage guide
│   │   │   ├── nexa/              # Nexa fonts folder
│   │   │   ├── poppins/           # Poppins fonts folder
│   │   │   └── montserrat/        # Montserrat fonts folder
│   │   ├── css/styles.css         # Updated with font integration
│   │   └── js/carousel.js
│   ├── templates/main/
│   │   ├── base.html              # Updated with fonts & Font Awesome
│   │   ├── create_payment.html    # Payment method selection
│   │   ├── process_payment.html   # Payment processing
│   │   ├── payment_success.html   # Success confirmation
│   │   └── payment_pending.html   # Pending status
│   ├── models.py                  # Updated with payment models
│   ├── views.py                   # Updated with payment views
│   └── urls.py                    # Updated with payment routes
└── init_payment_methods.py        # Payment method initialization script
```

## 🔧 Database Migrations
- Migration `0004_payment_paymentmethod_paymentcallback_and_more.py` created
- All payment models are now available in the database
- Payment methods need to be created manually (see below)

## ⚙️ Setup Instructions

1. **Apply migrations**:
   ```bash
   cd stationeryworld
   python manage.py migrate
   ```

2. **Create payment methods** (using Django shell):
   ```bash
   python manage.py shell
   ```
   Then run:
   ```python
   from main.models import PaymentMethod
   from decimal import Decimal
   
   # Create payment methods
   PaymentMethod.objects.get_or_create(
       provider='mtn',
       defaults={'name': 'MTN Mobile Money', 'processing_fee': Decimal('500.00'), 'is_active': True}
   )
   PaymentMethod.objects.get_or_create(
       provider='airtel',
       defaults={'name': 'Airtel Money', 'processing_fee': Decimal('500.00'), 'is_active': True}
   )
   PaymentMethod.objects.get_or_create(
       provider='card',
       defaults={'name': 'Credit/Debit Card', 'processing_fee': Decimal('1000.00'), 'is_active': True}
   )
   PaymentMethod.objects.get_or_create(
       provider='bank',
       defaults={'name': 'Bank Transfer', 'processing_fee': Decimal('0.00'), 'is_active': True}
   )
   PaymentMethod.objects.get_or_create(
       provider='cash',
       defaults={'name': 'Cash on Delivery', 'processing_fee': Decimal('0.00'), 'is_active': True}
   )
   ```

## 🎨 Customization

### Adding New Payment Methods
1. Add to the payment method choices in `models.py`
2. Create corresponding processing logic in `views.py`
3. Update templates to handle the new method

### Adding New Fonts
1. Download font files
2. Place in appropriate folder
3. Update `fonts.css` with new font-face declarations
4. Reference in CSS with `font-family: 'FontName', sans-serif;`

## 🔗 Integration Points

- **Order to Payment**: `/payment/create/<order_id>/` creates payment from existing orders
- **Payment Processing**: Handles multiple payment providers through unified interface
- **Callback Handling**: `/payment/callback/` receives payment provider notifications
- **Status Tracking**: Complete payment lifecycle from creation to completion

The system is now ready for production use with real payment provider integrations!