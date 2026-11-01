# store/urls.py - URL routing for catalog, cart, wishlist, and account views
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # 1. Catalog & Showcase
    path('', views.home_view, name='home'),
    path('products/', views.products_view, name='products'),
    path('product/<str:product_id>/', views.product_detail_view, name='product_detail'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),

    # 2. Shopping Cart (Page + Optimized Backend AJAX Endpoints)
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/update/', views.update_cart_view, name='update_cart'),
    path('cart/remove/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart_view, name='clear_cart'),
    path('cart/data/', views.get_cart_data_view, name='cart_data'),

    # 3. Wishlist (Page + Optimized Backend AJAX Endpoints)
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/', views.toggle_wishlist_view, name='toggle_wishlist'),
    path('wishlist/data/', views.get_wishlist_data_view, name='wishlist_data'),

    # 4. Customer Account & Auth
    path('myorders/', views.order_history_view, name='myorders'),
    path('orders/', views.order_history_view, name='order_history'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
