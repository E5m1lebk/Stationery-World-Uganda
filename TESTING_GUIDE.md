# 🧪 Stationery World Uganda - Testing Guide

## 📋 Application Status: ✅ READY FOR TESTING

### 🔧 **System Setup Complete:**
- ✅ Django Development Server: Running on `http://127.0.0.1:8000/`
- ✅ SQLite Database: Configured and populated with test data
- ✅ Cash on Delivery: Only payment method enabled
- ✅ Social Media Links: Added to footer
- ✅ Test Products: 16 products available for testing

---

## 🚀 **Testing URLs**

### **Core Pages:**
- **Homepage**: http://127.0.0.1:8000/
- **Products**: http://127.0.0.1:8000/products/
- **Services**: http://127.0.0.1:8000/services/
- **Contact**: http://127.0.0.1:8000/contact/

### **Cash on Delivery Flow:**
1. Visit Products page → Select a product → Click "Order Now"
2. Fill customer details (Name, Phone, Quantity)
3. Submit order → Redirected to Cash on Delivery Confirmation
4. Confirm order → Payment marked as "Processing"
5. Order completion message displayed

---

## 🛒 **Cash on Delivery Testing Steps**

### **Test Scenario 1: Complete Order Flow**
1. **Navigate to Products**: http://127.0.0.1:8000/products/
2. **Select Product**: Click on any product (e.g., "A4 Writing Pad")
3. **Fill Order Form**:
   - Customer Name: `John Doe`
   - Phone Number: `+256700123456`
   - Quantity: `2`
4. **Submit Order**: Click "Place Order"
5. **Verify Confirmation**: Should show Cash on Delivery confirmation page
6. **Check Details**:
   - Product information displayed correctly
   - Total amount calculated (price × quantity)
   - Cash on delivery instructions visible
7. **Confirm Order**: Click "Confirm Order for Cash on Delivery"
8. **Verify Success**: Should show success message with order details

### **Test Scenario 2: Order Multiple Products**
1. **Create Orders**:
   - A4 Writing Pad × 1 = UGX 15,000
   - USB Flash Drive × 1 = UGX 45,000
   - Ballpoint Pens × 2 = UGX 50,000
2. **Verify Each Order**:
   - Order details accurate
   - No processing fees applied
   - Customer contact information preserved

---

## 📱 **Social Media Testing**

### **Footer Social Links Verification:**
1. **Check Footer**: Scroll to bottom of any page
2. **Verify Links Present**:
   - YouTube icon → Links to YouTube channel
   - WhatsApp icon → Opens WhatsApp contact
   - Facebook icon → Links to Facebook page
   - Instagram icon → Links to Instagram profile
   - TikTok icon → Links to TikTok profile
3. **Test Responsiveness**: Check on mobile and desktop views

---

## 🗄️ **Database Testing**

### **Available Test Data:**
- **Products**: 16 items across categories:
  - Stationery (Pads, Pens, Organizers)
  - Electronics (USB drives)
  - Design Services
  - Printing Services
- **Price Range**: UGX 15,000 - UGX 150,000
- **Payment Method**: Only "Cash on Delivery" enabled

### **Database Verification Commands:**
```bash
cd stationeryworld
python manage.py shell
# Inside shell:
from main.models import Product, Order, PaymentMethod
print(f"Products: {Product.objects.count()}")
print(f"Payment Methods: {PaymentMethod.objects.count()}")
print(PaymentMethod.objects.filter(provider='cash').first())
```

---

## 🔍 **Manual Testing Checklist**

### **✅ Frontend Testing:**
- [ ] Homepage loads correctly
- [ ] Navigation menu works
- [ ] Product listing displays properly
- [ ] Product detail pages show correctly
- [ ] Contact form functions
- [ ] Social media links in footer work
- [ ] Responsive design on mobile

### **✅ Cash on Delivery Flow:**
- [ ] Order form accepts valid inputs
- [ ] Order form rejects invalid inputs
- [ ] Cash on delivery confirmation page displays correctly
- [ ] Order details calculated properly
- [ ] Success message shows after order completion
- [ ] No payment processing required

### **✅ Backend Testing:**
- [ ] Database saves orders correctly
- [ ] Payment records created with 'processing' status
- [ ] Customer information stored properly
- [ ] Order quantities calculated correctly

---

## 🐛 **Common Testing Scenarios**

### **Edge Cases:**
1. **Large Quantity**: Order 100+ items
2. **Long Names**: Test with very long customer names
3. **Special Characters**: Test with special characters in names
4. **Empty Fields**: Verify form validation
5. **Network Issues**: Test behavior with slow connections

### **Mobile Testing:**
1. **Responsive Design**: Test on mobile devices
2. **Touch Interface**: Verify touch interactions work
3. **Form Input**: Test form filling on mobile
4. **Navigation**: Test mobile navigation menu

---

## 🚀 **Performance Testing**

### **Load Testing:**
- **Multiple Simultaneous Orders**: Open 5+ browser tabs and place orders
- **Database Performance**: Check response times with many products
- **Static Assets**: Verify CSS/JS loading speeds

### **Browser Compatibility:**
- **Chrome**: Primary testing browser
- **Firefox**: Cross-browser testing
- **Safari**: Mac compatibility
- **Edge**: Windows compatibility

---

## 📞 **Test Data for Quick Testing**

### **Sample Customer Details:**
- **Name**: `Jane Smith`
- **Phone**: `+256701234567`
- **Email**: `jane@example.com`

### **Sample Products for Testing:**
1. **A4 Writing Pad** - UGX 15,000
2. **USB Flash Drive 32GB** - UGX 45,000
3. **Graphic Design Services** - UGX 150,000

---

## 🎯 **Success Criteria**

### **✅ Testing Complete When:**
1. All order flows complete successfully
2. Cash on delivery confirmation works
3. Social media links open correctly
4. Database stores all order information
5. No payment processing errors
6. Mobile-responsive design works
7. Contact form sends emails
8. All products display correctly

---

## 🛠️ **Troubleshooting**

### **Common Issues:**
1. **Server Not Responding**: Restart with `python manage.py runserver`
2. **Database Errors**: Run `python manage.py migrate`
3. **Missing Products**: Run `python setup_test_data.py`
4. **Payment Method Issues**: Run `python init_payment_methods.py`

### **Debug Commands:**
```bash
# Check server status
curl http://127.0.0.1:8000/

# Check database
cd stationeryworld && python manage.py dbshell

# Reset database (if needed)
rm db.sqlite3
python manage.py migrate
python init_payment_methods.py
python setup_test_data.py
```

---

## 🎉 **Ready for Production**

The application is now configured with:
- ✅ **Cash on Delivery Only**: No complex payment processing
- ✅ **Social Media Integration**: All platforms linked
- ✅ **Test Data**: Ready for immediate testing
- ✅ **Responsive Design**: Works on all devices
- ✅ **Database**: SQLite with all required data

**Test the application now at**: http://127.0.0.1:8000/