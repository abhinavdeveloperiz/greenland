# store/urls.py
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.products_view, name='products'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('product/<str:product_id>/', views.product_detail_view, name='product_detail'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-confirmation/<str:order_id>/', views.order_confirmation_view, name='order_confirmation'),
    path('track-order/<str:order_id>/', views.order_tracking_view, name='order_tracking'),
    path('orders/', views.order_history_view, name='order_history'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]
