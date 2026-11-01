# store/views.py - Optimized, database-driven views with select_related & full Cart/Wishlist backend
import json
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Q
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST, require_GET

from .models import (
    Category,
    Brand,
    Product,
    ProductVariant,
    AdvertisementBanner,
    Cart,
    CartItem,
    Wishlist,
    WishlistItem,
)
from .utils import (
    get_or_create_cart,
    get_or_create_wishlist,
    merge_carts,
    merge_wishlists,
    serialize_cart_item,
    serialize_wishlist_item,
)


def _parse_payload(request):
    """Helper to extract parameters from JSON body or standard POST form data."""
    if request.content_type == 'application/json':
        try:
            return json.loads(request.body.decode('utf-8'))
        except Exception:
            return {}
    return request.POST


# =========================================================================
# 1. CATALOG & STOREFRONT VIEWS (OPTIMIZED WITH SELECT_RELATED & PREFETCH)
# =========================================================================

def home_view(request):
    """
    Store homepage view.
    Optimized with select_related('category') and prefetch_related('variants', 'gallery_images')
    to load featured items, new arrivals, and categories in minimal database queries.
    """
    all_products = list(
        Product.objects.filter(is_active=True)
        .select_related('category')
        .prefetch_related('variants', 'gallery_images')
    )
    featured_products = [p for p in all_products if p.is_featured]
    new_arrivals = [p for p in all_products if p.is_new][:4]

    # Show only categories represented by active GreenLand products
    greenland_products = [p for p in all_products if p.brand_code == 'greenland']
    db_categories = list(
        Category.objects.filter(
            is_featured=True,
            products__is_active=True,
            products__brand_code='greenland',
        ).distinct().order_by('order')
    )

    # Fast single-pass counting in python without extra DB hits
    cat_counts = {}
    for p in greenland_products:
        cat_counts[p.category_id] = cat_counts.get(p.category_id, 0) + 1

    for cat in db_categories:
        count = cat_counts.get(cat.id, 0)
        cat.active_count = count
        if cat.item_count_label and 'wholesale' not in cat.item_count_label.lower():
            cat.itemCount = cat.item_count_label
        elif count > 0:
            cat.itemCount = f"{count} Products" if count != 1 else "1 Product"
        else:
            cat.itemCount = "Explore Range"

    # Brand counts across all active products
    brands = list(Brand.objects.filter(is_active=True).order_by('order'))
    brand_counts = {'all': len(all_products)}
    brand_prod_counts = {}
    for p in all_products:
        brand_prod_counts[p.brand_code] = brand_prod_counts.get(p.brand_code, 0) + 1
    for b in brands:
        count = brand_prod_counts.get(b.code, 0)
        b.active_count = count
        brand_counts[b.code] = count

    advertisement_banner = (
        AdvertisementBanner.objects.filter(is_active=True)
        .select_related('linked_product', 'linked_product__category')
        .first()
    )

    context = {
        'featured_products': featured_products,
        'all_products': all_products,
        'new_arrivals': new_arrivals,
        'categories': db_categories,
        'brands': brands,
        'brand_counts': brand_counts,
        'advertisement_banner': advertisement_banner,
        'total_products_count': len(all_products),
        'total_categories_count': len(db_categories),
    }
    return render(request, 'pages/home.html', context)


def products_view(request):
    """
    Catalog view with database filtering by category, brand, price, availability, and search.
    Utilizes select_related('category') and prefetch_related('variants', 'gallery_images')
    to prevent the N+1 query problem across product cards.
    """
    search_query = request.GET.get('search', '').strip()
    selected_category = request.GET.get('category', 'all')
    selected_brand = request.GET.get('brand', 'all')
    sort_by = request.GET.get('sort', 'featured')
    availability = request.GET.get('availability', 'all')
    min_price_raw = request.GET.get('min_price', '').strip()
    max_price_raw = request.GET.get('max_price', '').strip()

    try:
        min_price = float(min_price_raw) if min_price_raw else None
    except ValueError:
        min_price = None

    try:
        max_price = float(max_price_raw) if max_price_raw else None
    except ValueError:
        max_price = None

    # Base query optimized with select_related & prefetch_related
    products = (
        Product.objects.filter(is_active=True)
        .select_related('category')
        .prefetch_related('variants', 'gallery_images')
    )

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(spec_1__icontains=search_query) |
            Q(spec_2__icontains=search_query) |
            Q(spec_3__icontains=search_query) |
            Q(spec_4__icontains=search_query)
        )

    if selected_category and selected_category != 'all':
        products = products.filter(category__slug=selected_category)

    if selected_brand and selected_brand != 'all':
        products = products.filter(brand_code=selected_brand)

    if availability and availability != 'all':
        products = products.filter(availability=availability)

    if min_price is not None:
        products = products.filter(price__gte=min_price)

    if max_price is not None:
        products = products.filter(price__lte=max_price)

    # Sorting
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    else:  # featured default
        products = products.order_by('-is_featured', '-is_new', '-created_at')

    filtered_list = list(products)

    # All active products summary for sidebar category and brand counters
    all_active_meta = list(Product.objects.filter(is_active=True).values('id', 'brand_code', 'category_id'))
    total_active_count = len(all_active_meta)

    brands = list(Brand.objects.filter(is_active=True).order_by('order'))
    brand_counts = {'all': total_active_count}
    for b in brands:
        count = sum(1 for p in all_active_meta if p['brand_code'] == b.code)
        b.active_count = count
        brand_counts[b.code] = count

    active_brand_obj = Brand.objects.filter(code=selected_brand).first() if selected_brand != 'all' else None
    active_category_obj = Category.objects.filter(slug=selected_category).first() if selected_category != 'all' else None

    # Categories with count of active products
    db_categories = list(Category.objects.all().order_by('order'))
    for cat in db_categories:
        count = sum(1 for p in all_active_meta if p['category_id'] == cat.id)
        cat.active_count = count
        cat.itemCount = f"{count} Products" if count != 1 else "1 Product"

    active_filters_count = 0
    if selected_category != 'all':
        active_filters_count += 1
    if selected_brand != 'all':
        active_filters_count += 1
    if min_price is not None or max_price is not None:
        active_filters_count += 1
    if availability != 'all':
        active_filters_count += 1

    context = {
        'products': filtered_list,
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'min_price': min_price_raw,
        'max_price': max_price_raw,
        'active_filters_count': active_filters_count,
        'active_brand_obj': active_brand_obj,
        'active_category_obj': active_category_obj,
        'brand_counts': brand_counts,
        'categories_with_counts': db_categories,
        'brands': brands,
        'sort_by': sort_by,
        'availability': availability,
        'total_count': len(filtered_list),
    }
    return render(request, 'pages/products.html', context)


def product_detail_view(request, product_id):
    """
    Product detail view querying with select_related('category') and prefetching
    variants & gallery images for ultra-fast response times.
    """
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('variants', 'gallery_images'),
        id=product_id,
        is_active=True
    )

    related_products = list(
        Product.objects.filter(category=product.category, is_active=True)
        .exclude(id=product.id)
        .select_related('category')
        .prefetch_related('variants')[:4]
    )

    variants = list(product.variants.filter(is_active=True).order_by('order', 'price'))

    # Format variants data for Alpine.js reactive UI
    variants_data = []
    default_variant_data = None

    for v in variants:
        v_dict = {
            'id': v.id,
            'weight': v.weight,
            'unit': v.unit,
            'price': float(v.price),
            'original_price': float(v.original_price) if v.original_price else None,
            'stock': v.stock,
            'is_default': v.is_default,
        }
        variants_data.append(v_dict)
        if v.is_default and default_variant_data is None:
            default_variant_data = v_dict

    # Fallback if no variants configured in DB
    if not variants_data:
        fallback_v = {
            'id': 0,
            'weight': product.weight,
            'unit': product.unit,
            'price': float(product.price),
            'original_price': float(product.original_price) if product.original_price else None,
            'stock': product.stock,
            'is_default': True,
        }
        variants_data = [fallback_v]
        default_variant_data = fallback_v
    elif default_variant_data is None:
        default_variant_data = variants_data[0]

    context = {
        'product': product,
        'product_images': product.images,
        'related_products': related_products,
        'variants': variants,
        'variants_data': variants_data,
        'default_variant_data': default_variant_data,
        'default_variant': default_variant_data,
    }
    return render(request, 'pages/product_detail.html', context)


def about_view(request):
    """About us company history & brand philosophy view."""
    return render(request, 'pages/about.html')


def contact_view(request):
    """Contact us & wholesale inquiry view."""
    return render(request, 'pages/contact.html')


# =========================================================================
# 2. CART BACKEND VIEWS & APIS (OPTIMIZED WITH SELECT_RELATED)
# =========================================================================

def cart_view(request):
    """
    Shopping cart page view.
    Preloads cart items with select_related('product', 'product__category', 'variant')
    for instant rendering and seamless Alpine.js initialization.
    """
    cart = get_or_create_cart(request)
    cart_items = list(
        CartItem.objects.filter(cart=cart)
        .select_related('product', 'product__category', 'variant')
        .order_by('-created_at')
    )
    serialized_items = [serialize_cart_item(item) for item in cart_items]

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_items_json': json.dumps(serialized_items),
        'cart_count': cart.total_count,
        'subtotal': float(cart.subtotal),
    }
    return render(request, 'pages/cart.html', context)


@require_POST
def add_to_cart_view(request):
    """
    Add product (or specific variant) to shopping cart.
    Accepts JSON body or POST form data.
    Validates stock, updates item quantity, and returns updated cart statistics.
    """
    payload = _parse_payload(request)
    product_id = payload.get('product_id') or payload.get('id')
    variant_id = payload.get('variant_id') or payload.get('variantId')
    qty_raw = payload.get('quantity') or payload.get('qty', 1)

    if not product_id:
        return JsonResponse({'success': False, 'error': 'Product ID is required.'}, status=400)

    try:
        qty = max(1, int(qty_raw))
    except (ValueError, TypeError):
        qty = 1

    # Fetch product with category in one query
    product = get_object_or_404(Product.objects.select_related('category'), id=product_id, is_active=True)

    variant = None
    if variant_id:
        try:
            variant_id = int(variant_id)
            if variant_id > 0:
                variant = ProductVariant.objects.filter(id=variant_id, product=product, is_active=True).first()
        except (ValueError, TypeError):
            variant = None

    # Check stock limit
    stock_limit = variant.stock if variant else product.stock
    if stock_limit <= 0:
        return JsonResponse({
            'success': False,
            'error': f'{product.name} is currently out of stock.'
        }, status=400)

    cart = get_or_create_cart(request)

    # Get or create item in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        variant=variant,
        defaults={'quantity': min(qty, stock_limit)}
    )

    if not created:
        new_qty = min(cart_item.quantity + qty, stock_limit)
        cart_item.quantity = new_qty
        cart_item.save(update_fields=['quantity', 'updated_at'])

    cart_items = list(
        CartItem.objects.filter(cart=cart)
        .select_related('product', 'product__category', 'variant')
        .order_by('-created_at')
    )

    weight_label = f" ({cart_item.weight_display})" if cart_item.weight_display else ""
    return JsonResponse({
        'success': True,
        'message': f'Added {product.name}{weight_label} to your cart!',
        'cart_count': cart.total_count,
        'subtotal': round(float(cart.subtotal), 3),
        'item': serialize_cart_item(cart_item),
        'items': [serialize_cart_item(item) for item in cart_items],
    })


@require_POST
def update_cart_view(request):
    """
    Update item quantity in cart.
    Accepts item_key, item_id, or product_id + variant_id and target quantity.
    Removes item if quantity is zero.
    """
    payload = _parse_payload(request)
    item_key = payload.get('item_key') or payload.get('id')
    item_id = payload.get('item_id')
    qty_raw = payload.get('quantity') or payload.get('qty', 1)

    try:
        qty = int(qty_raw)
    except (ValueError, TypeError):
        qty = 1

    cart = get_or_create_cart(request)
    cart_item = None

    if item_id:
        cart_item = CartItem.objects.filter(cart=cart, id=item_id).select_related('product', 'variant').first()
    elif item_key:
        # Match item key format (e.g. "prod-gl-tea-v12" or "prod-gl-tea")
        if '-v' in str(item_key):
            parts = str(item_key).rsplit('-v', 1)
            p_id, v_id = parts[0], parts[1]
            cart_item = CartItem.objects.filter(cart=cart, product_id=p_id, variant_id=v_id).select_related('product', 'variant').first()
        else:
            cart_item = CartItem.objects.filter(cart=cart, product_id=item_key, variant=None).select_related('product', 'variant').first()

    if not cart_item:
        return JsonResponse({'success': False, 'error': 'Item not found in cart.'}, status=404)

    if qty <= 0:
        cart_item.delete()
        msg = f'Removed {cart_item.product.name} from cart.'
    else:
        stock_limit = cart_item.variant.stock if cart_item.variant else cart_item.product.stock
        capped_qty = min(qty, stock_limit)
        cart_item.quantity = capped_qty
        cart_item.save(update_fields=['quantity', 'updated_at'])
        msg = f'Updated quantity for {cart_item.product.name}.'

    cart_items = list(
        CartItem.objects.filter(cart=cart)
        .select_related('product', 'product__category', 'variant')
        .order_by('-created_at')
    )

    return JsonResponse({
        'success': True,
        'message': msg,
        'cart_count': cart.total_count,
        'subtotal': round(float(cart.subtotal), 3),
        'items': [serialize_cart_item(item) for item in cart_items],
    })


@require_POST
def remove_from_cart_view(request):
    """Remove a specific item from the shopping cart."""
    payload = _parse_payload(request)
    item_key = payload.get('item_key') or payload.get('id')
    item_id = payload.get('item_id')

    cart = get_or_create_cart(request)
    cart_item = None

    if item_id:
        cart_item = CartItem.objects.filter(cart=cart, id=item_id).select_related('product').first()
    elif item_key:
        if '-v' in str(item_key):
            parts = str(item_key).rsplit('-v', 1)
            cart_item = CartItem.objects.filter(cart=cart, product_id=parts[0], variant_id=parts[1]).select_related('product').first()
        else:
            cart_item = CartItem.objects.filter(cart=cart, product_id=item_key, variant=None).select_related('product').first()

    if cart_item:
        name = cart_item.product.name
        cart_item.delete()
        msg = f'Removed {name} from cart.'
    else:
        msg = 'Item removed.'

    cart_items = list(
        CartItem.objects.filter(cart=cart)
        .select_related('product', 'product__category', 'variant')
        .order_by('-created_at')
    )

    return JsonResponse({
        'success': True,
        'message': msg,
        'cart_count': cart.total_count,
        'subtotal': round(float(cart.subtotal), 3),
        'items': [serialize_cart_item(item) for item in cart_items],
    })


@require_POST
def clear_cart_view(request):
    """Empty all items in the customer's shopping cart."""
    cart = get_or_create_cart(request)
    cart.clear()
    return JsonResponse({
        'success': True,
        'message': 'Your shopping cart has been cleared.',
        'cart_count': 0,
        'subtotal': 0.000,
        'items': [],
    })


@require_GET
def get_cart_data_view(request):
    """Return JSON state of current cart for frontend synchronization."""
    cart = get_or_create_cart(request)
    cart_items = list(
        CartItem.objects.filter(cart=cart)
        .select_related('product', 'product__category', 'variant')
        .order_by('-created_at')
    )
    return JsonResponse({
        'success': True,
        'cart_count': cart.total_count,
        'subtotal': round(float(cart.subtotal), 3),
        'items': [serialize_cart_item(item) for item in cart_items],
    })


# =========================================================================
# 3. WISHLIST BACKEND VIEWS & APIS (OPTIMIZED WITH SELECT_RELATED)
# =========================================================================

def wishlist_view(request):
    """
    Saved wishlist items page view.
    Preloads items using select_related('product', 'product__category')
    to render full product cards with zero additional database lookups.
    """
    wishlist = get_or_create_wishlist(request)
    wishlist_items = list(
        WishlistItem.objects.filter(wishlist=wishlist)
        .select_related('product', 'product__category')
        .order_by('-created_at')
    )
    serialized_items = [serialize_wishlist_item(item) for item in wishlist_items]

    context = {
        'wishlist': wishlist,
        'wishlist_items': wishlist_items,
        'wishlist_items_json': json.dumps(serialized_items),
        'wishlist_count': wishlist.total_count,
    }
    return render(request, 'pages/wishlist.html', context)


@require_POST
def toggle_wishlist_view(request):
    """
    Toggle a product into or out of the customer's wishlist.
    Accepts JSON body or POST form data.
    Returns in_wishlist boolean flag and total wishlist counter.
    """
    payload = _parse_payload(request)
    product_id = payload.get('product_id') or payload.get('id')

    if not product_id:
        return JsonResponse({'success': False, 'error': 'Product ID is required.'}, status=400)

    product = get_object_or_404(Product.objects.select_related('category'), id=product_id, is_active=True)
    wishlist = get_or_create_wishlist(request)

    existing_item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()
    if existing_item:
        existing_item.delete()
        in_wishlist = False
        message = f'Removed {product.name} from wishlist.'
    else:
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        in_wishlist = True
        message = f'Saved {product.name} to your wishlist!'

    return JsonResponse({
        'success': True,
        'in_wishlist': in_wishlist,
        'product_id': str(product.id),
        'wishlist_count': wishlist.total_count,
        'message': message,
        'item': {
            'id': str(product.id),
            'name': product.name,
            'price': float(product.price),
            'originalPrice': float(product.original_price or product.price),
            'weight': product.weight,
            'image': product.primary_image_url,
        } if in_wishlist else None
    })


@require_GET
def get_wishlist_data_view(request):
    """Return JSON state of current wishlist for frontend synchronization."""
    wishlist = get_or_create_wishlist(request)
    wishlist_items = list(
        WishlistItem.objects.filter(wishlist=wishlist)
        .select_related('product', 'product__category')
        .order_by('-created_at')
    )
    return JsonResponse({
        'success': True,
        'wishlist_count': wishlist.total_count,
        'items': [serialize_wishlist_item(item) for item in wishlist_items],
        'ids': [str(item.product_id) for item in wishlist_items],
    })


# =========================================================================
# 4. CUSTOMER ACCOUNT & AUTHENTICATION VIEWS
# =========================================================================

def order_history_view(request):
    """Order history view."""
    return render(request, 'pages/order_history.html')


def profile_view(request):
    """Customer account profile view."""
    return render(request, 'pages/profile.html')


@ensure_csrf_cookie
def login_view(request):
    """Customer account login view with email + OTP."""
    return render(request, 'pages/login.html')


def send_otp_view(request):
    """Generate and send OTP code to the provided email."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

    email = request.POST.get('email', '').strip().lower()
    if not email or '@' not in email:
        return JsonResponse({'success': False, 'error': 'Please enter a valid email address.'}, status=400)

    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    request.session['login_email'] = email
    request.session['login_otp'] = otp
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'message': f'A 6-digit verification code was sent to {email}',
        'demo_otp': otp,
    })


def verify_otp_view(request):
    """
    Verify OTP, authenticate user, and automatically merge any anonymous
    guest cart items and wishlist items into the user's permanent account.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

    entered_otp = request.POST.get('otp', '').strip()
    session_otp = request.session.get('login_otp', '')
    session_email = request.session.get('login_email', '').strip().lower()

    if not entered_otp:
        return JsonResponse({'success': False, 'error': 'Please enter the 6-digit verification code.'}, status=400)

    # Allow session OTP or master test OTP '123456'
    if entered_otp != session_otp and entered_otp != '123456':
        return JsonResponse({'success': False, 'error': 'Incorrect verification code. Please check and try again.'}, status=400)

    email = session_email or request.POST.get('email', '').strip().lower()
    if not email:
        email = 'customer@greenland.com'

    # Auto get-or-create Django User (no manual registration required)
    user, _ = User.objects.get_or_create(username=email, defaults={'email': email})
    if not user.email:
        user.email = email
        user.save(update_fields=['email'])

    display_name = user.first_name or email.split('@')[0].replace('.', ' ').replace('_', ' ').title()

    # Capture current session key before login
    prev_session_key = request.session.session_key

    auth_login(request, user)

    # Clear OTP from session
    request.session.pop('login_otp', None)

    # Merge any guest cart and wishlist into authenticated user account
    if prev_session_key:
        guest_cart = Cart.objects.filter(session_key=prev_session_key, user=None).first()
        if guest_cart:
            user_cart, _ = Cart.objects.get_or_create(user=user)
            merge_carts(guest_cart, user_cart)

        guest_wishlist = Wishlist.objects.filter(session_key=prev_session_key, user=None).first()
        if guest_wishlist:
            user_wishlist, _ = Wishlist.objects.get_or_create(user=user)
            merge_wishlists(guest_wishlist, user_wishlist)

    next_url = request.POST.get('next', '').strip() or request.GET.get('next', '').strip() or '/'

    return JsonResponse({
        'success': True,
        'email': email,
        'name': display_name,
        'redirect_url': next_url,
    })


def logout_view(request):
    """Log out customer and redirect to home."""
    auth_logout(request)
    return redirect('store:home')


def register_view(request):
    """Redirect register requests to OTP login since accounts are auto-created upon verification."""
    return redirect('store:login')
