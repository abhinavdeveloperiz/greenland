# store/utils.py - Cart & Wishlist helpers and serialization
from .models import Cart, CartItem, Wishlist, WishlistItem


def get_session_key(request):
    """Ensure session exists and return the session key."""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_or_create_cart(request):
    """
    Get or create a Cart for the current user or session.
    Automatically links to authenticated user and merges unattached guest carts.
    """
    session_key = get_session_key(request)
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        # Check if there was an active guest cart created before logging in
        if session_key:
            guest_cart = Cart.objects.filter(session_key=session_key, user=None).first()
            if guest_cart and guest_cart != cart:
                merge_carts(guest_cart, cart)
        return cart
    else:
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
        return cart


def get_or_create_wishlist(request):
    """
    Get or create a Wishlist for the current user or session.
    Automatically links to authenticated user and merges unattached guest wishlists.
    """
    session_key = get_session_key(request)
    if request.user.is_authenticated:
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        if session_key:
            guest_wishlist = Wishlist.objects.filter(session_key=session_key, user=None).first()
            if guest_wishlist and guest_wishlist != wishlist:
                merge_wishlists(guest_wishlist, wishlist)
        return wishlist
    else:
        wishlist, _ = Wishlist.objects.get_or_create(session_key=session_key, user=None)
        return wishlist


def merge_carts(source_cart, target_cart):
    """Merge items from source_cart into target_cart, then delete source_cart."""
    source_items = CartItem.objects.filter(cart=source_cart).select_related('product', 'variant')
    for item in source_items:
        target_item, created = CartItem.objects.get_or_create(
            cart=target_cart,
            product=item.product,
            variant=item.variant,
            defaults={'quantity': item.quantity}
        )
        if not created:
            target_item.quantity += item.quantity
            target_item.save(update_fields=['quantity', 'updated_at'])
    source_cart.delete()


def merge_wishlists(source_wishlist, target_wishlist):
    """Merge items from source_wishlist into target_wishlist, then delete source_wishlist."""
    source_items = WishlistItem.objects.filter(wishlist=source_wishlist)
    for item in source_items:
        WishlistItem.objects.get_or_create(
            wishlist=target_wishlist,
            product=item.product
        )
    source_wishlist.delete()


def serialize_cart_item(item):
    """Format a CartItem for JSON API responses and frontend state."""
    stock_limit = item.variant.stock if item.variant else item.product.stock
    return {
        'id': item.item_key,
        'itemId': item.id,
        'productId': str(item.product_id),
        'variantId': item.variant_id,
        'name': item.product.name,
        'price': float(item.unit_price),
        'originalPrice': float(item.original_price),
        'weight': item.weight_display,
        'image': item.image_url,
        'quantity': item.quantity,
        'stock': stock_limit,
        'subtotal': round(float(item.total_price), 3),
    }


def serialize_wishlist_item(item):
    """Format a WishlistItem for JSON API responses and frontend state."""
    product = item.product
    return {
        'id': str(product.id),
        'name': product.name,
        'price': float(product.price),
        'originalPrice': float(product.original_price or product.price),
        'weight': product.weight,
        'image': product.primary_image_url,
    }

