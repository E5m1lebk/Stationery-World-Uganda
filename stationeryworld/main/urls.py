from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('order/', views.order, name='order'),
    # Payment URLs
    path('payment/create/<int:order_id>/', views.create_payment, name='create_payment'),
    path('payment/process/<int:payment_id>/', views.process_payment, name='process_payment'),
    path('payment/success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('payment/pending/<int:payment_id>/', views.payment_pending, name='payment_pending'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    # Admin URLs
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/update-content/', views.admin_update_content, name='admin_update_content'),
    path('admin/update-contact/', views.admin_update_contact, name='admin_update_contact'),
    path('admin/update-services/', views.admin_update_services, name='admin_update_services'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
]
