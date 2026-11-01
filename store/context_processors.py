# store/context_processors.py - Dynamic database context processor
from .models import Category, Brand, Cart, Wishlist
from .static_data import CATEGORIES as STATIC_CATEGORIES, BRANDS as STATIC_BRANDS

def global_store_context(request):
    """Global context processor providing categories, brands, and live cart/wishlist counters."""
    try:
        categories = list(Category.objects.all().order_by('order'))
        if not categories:
            categories = STATIC_CATEGORIES
    except Exception:
        categories = STATIC_CATEGORIES

    try:
        brands = list(Brand.objects.filter(is_active=True).order_by('order'))
        if not brands:
            brands = STATIC_BRANDS
    except Exception:
        brands = STATIC_BRANDS

    cart_count = 0
    cart_subtotal = 0.0
    wishlist_count = 0

    try:
        session_key = request.session.session_key
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            wishlist = Wishlist.objects.filter(user=request.user).first()
        elif session_key:
            cart = Cart.objects.filter(session_key=session_key, user=None).first()
            wishlist = Wishlist.objects.filter(session_key=session_key, user=None).first()
        else:
            cart = None
            wishlist = None

        if cart:
            cart_count = cart.total_count
            cart_subtotal = float(cart.subtotal)
        if wishlist:
            wishlist_count = wishlist.total_count
    except Exception:
        pass

    return {
        'CATEGORIES': categories,
        'GLOBAL_BRANDS': brands,
        'server_cart_count': cart_count,
        'server_cart_subtotal': cart_subtotal,
        'server_wishlist_count': wishlist_count,
    }
