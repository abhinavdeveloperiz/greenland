# store/urls.py
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # 1. Home
    path('', views.home_view, name='home'),
    # 2. Products
    path('products/', views.products_view, name='products'),
    # 3. Product Details
    path('product/<str:product_id>/', views.product_detail_view, name='product_detail'),
    # 4. About
    path('about/', views.about_view, name='about'),
    # 5. Contact
    path('contact/', views.contact_view, name='contact'),
    # 6. Cart
    path('cart/', views.cart_view, name='cart'),
    # 7. Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    # 8. My Orders
    path('myorders/', views.order_history_view, name='myorders'),
    path('orders/', views.order_history_view, name='order_history'),
    # 9. Profile
    path('profile/', views.profile_view, name='profile'),
    # 10. Login (Email + OTP)
    path('login/', views.login_view, name='login'),
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
    # 11. Register (Redirects to OTP login)
    path('register/', views.register_view, name='register'),
]
