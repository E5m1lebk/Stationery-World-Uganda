# Stationery World Uganda - Email Integration Setup Guide

## Overview
This guide explains the email integration and font styling changes made to the Stationery World Uganda website.

## Changes Implemented

### 1. Nexa Bold Font Styling
- Applied Nexa Bold font to all block words including:
  - All heading elements (h1, h2, h3, h4, h5, h6)
  - Display classes (display-1 through display-4)
  - Navigation brand elements
  - Hero section headings
  - Card titles
  - Button elements
  - Blockquotes and lead text

**Files Modified:**
- `stationeryworld/main/static/css/styles.css`

### 2. Email Integration
- Enhanced contact form functionality
- Added email sending capability to Stationery World
- Improved form field validation and structure

**Files Modified:**
- `stationeryworld/main/templates/main/contact.html` - Fixed form field names and types
- `stationeryworld/main/views.py` - Added email sending functionality
- `stationeryworld/stationaryworld/settings.py` - Added email configuration

## Current Email Setup (Development)

The website currently uses Django's console email backend, which means:
- Emails are printed to the console/terminal instead of being sent
- Perfect for development and testing
- No actual emails are sent

## Production Email Configuration

For production deployment, you need to configure a real email backend. Here are the most common options:

### Option 1: Gmail SMTP (Recommended for Small Businesses)

Add these settings to your `settings.py` file:

```python
# Gmail SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Replace with your Gmail address
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not regular password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
STATIONERY_WORLD_EMAIL = 'info@stationeryworld.ug'  # Your business email
```

**Important:** You must:
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password for your application
3. Use the App Password in `EMAIL_HOST_PASSWORD`

### Option 2: SendGrid (Recommended for Business)

```python
# SendGrid Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  # Always 'apikey' for SendGrid
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'  # Your SendGrid API key
DEFAULT_FROM_EMAIL = 'info@stationeryworld.ug'
STATIONERY_WORLD_EMAIL = 'info@stationeryworld.ug'
```

### Option 3: Amazon SES

```python
# Amazon SES Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.region.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-ses-smtp-username'
EMAIL_HOST_PASSWORD = 'your-ses-smtp-password'
DEFAULT_FROM_EMAIL = 'info@stationeryworld.ug'
STATIONERY_WORLD_EMAIL = 'info@stationeryworld.ug'
```

### Option 4: Custom SMTP Server

```python
# Custom SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587  # or 465 for SSL
EMAIL_USE_TLS = True  # Set to False if using SSL
EMAIL_USE_SSL = False  # Set to True if using port 465
EMAIL_HOST_USER = 'your-username'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'info@stationeryworld.ug'
STATIONERY_WORLD_EMAIL = 'info@stationeryworld.ug'
```

## Testing Email Functionality

### Development Testing
1. Run the development server: `python manage.py runserver`
2. Navigate to the contact page
3. Submit the contact form
4. Check your terminal/console for the email output

### Production Testing
1. Configure production email settings
2. Deploy your website
3. Submit the contact form from the live website
4. Check the recipient email (info@stationeryworld.ug) for the message

## Troubleshooting

### Common Issues:

1. **Authentication Errors:**
   - Verify username and password
   - For Gmail, ensure you're using an App Password
   - Check if 2FA is enabled where required

2. **Connection Errors:**
   - Verify server addresses and ports
   - Check firewall settings
   - Ensure SSL/TLS settings are correct

3. **Email Not Received:**
   - Check spam/junk folders
   - Verify recipient email address
   - Ensure sender email domain is not blocked

### Debug Mode
For debugging email issues, you can temporarily enable email logging:

Add this to your `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.core.mail': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Security Notes

1. **Never commit email passwords to version control**
2. **Use environment variables for sensitive data:**
   ```python
   import os
   EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
   ```
3. **Use App Passwords where available (Gmail, etc.)**
4. **Enable 2-factor authentication on email accounts**

## Next Steps

1. Choose your preferred email provider
2. Update `settings.py` with production email configuration
3. Test the contact form functionality
4. Monitor email delivery and adjust settings as needed

For additional support, contact your web hosting provider or email service provider for specific configuration help.