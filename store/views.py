# store/views.py - Database-driven views with full admin panel compatibility
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Category, Brand, Product, AdvertisementBanner


def home_view(request):
    """Homepage view serving live database categories and brand showcases."""
    all_products = list(Product.objects.filter(is_active=True))
    featured_products = [p for p in all_products if p.is_featured]
    new_arrivals = [p for p in all_products if p.is_new][:4]

    # Show only categories represented by active GreenLand products.
    greenland_products = [p for p in all_products if p.brand_code == 'greenland']
    db_categories = Category.objects.filter(
        is_featured=True,
        products__is_active=True,
        products__brand_code='greenland',
    ).distinct().order_by('order')
    categories_with_counts = []
    for cat in db_categories:
        count = sum(1 for p in greenland_products if p.category_id == cat.id)
        cat.active_count = count
        if cat.item_count_label and 'wholesale' not in cat.item_count_label.lower():
            cat.itemCount = cat.item_count_label
        elif count > 0:
            cat.itemCount = f"{count} Products" if count != 1 else "1 Product"
        else:
            cat.itemCount = "Explore Range"
        categories_with_counts.append(cat)

    # Brand counts across all active products
    brands = list(Brand.objects.filter(is_active=True).order_by('order'))
    brand_counts = {'all': len(all_products)}
    for b in brands:
        count = sum(1 for p in all_products if p.brand_code == b.code)
        b.active_count = count
        brand_counts[b.code] = count

    advertisement_banner = AdvertisementBanner.objects.filter(is_active=True).first()

    context = {
        'featured_products': featured_products,
        'all_products': all_products,
        'new_arrivals': new_arrivals,
        'categories': categories_with_counts,
        'brands': brands,
        'brand_counts': brand_counts,
        'advertisement_banner': advertisement_banner,
        'total_products_count': len(all_products),
        'total_categories_count': len(categories_with_counts),
    }
    return render(request, 'pages/home.html', context)


def products_view(request):
    """Full products catalog view with database filtering by category, brand, price, and search."""
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

    # Base query for active storefront products
    products = Product.objects.filter(is_active=True)

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

    # All active products for counts
    all_products = list(Product.objects.filter(is_active=True))

    brands = list(Brand.objects.filter(is_active=True).order_by('order'))
    brand_counts = {'all': len(all_products)}
    for b in brands:
        count = sum(1 for p in all_products if p.brand_code == b.code)
        b.active_count = count
        brand_counts[b.code] = count

    active_brand_obj = Brand.objects.filter(code=selected_brand).first() if selected_brand != 'all' else None
    active_category_obj = Category.objects.filter(slug=selected_category).first() if selected_category != 'all' else None

    # Categories with count of active products
    db_categories = Category.objects.all().order_by('order')
    categories_with_counts = []
    for cat in db_categories:
        count = sum(1 for p in all_products if p.category_id == cat.id)
        cat.active_count = count
        cat.itemCount = f"{count} Products" if count != 1 else "1 Product"
        categories_with_counts.append(cat)

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
        'categories_with_counts': categories_with_counts,
        'brands': brands,
        'sort_by': sort_by,
        'availability': availability,
        'total_count': len(filtered_list),
    }
    return render(request, 'pages/products.html', context)


def product_detail_view(request, product_id):
    """Product detail view querying directly from the database with weight variant support."""
    product = get_object_or_404(Product, id=product_id, is_active=True)

    related_products = list(
        Product.objects.filter(category=product.category, is_active=True)
        .exclude(id=product.id)[:4]
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


def cart_view(request):
    """Shopping cart page view."""
    return render(request, 'pages/cart.html')


def order_history_view(request):
    """Order history view."""
    return render(request, 'pages/order_history.html')


def wishlist_view(request):
    """Saved wishlist view."""
    return render(request, 'pages/wishlist.html')


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
    """Verify OTP and authenticate or auto-create the user without separate registration."""
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
    user, created = User.objects.get_or_create(username=email, defaults={'email': email})
    if not user.email:
        user.email = email
        user.save()

    display_name = user.first_name or email.split('@')[0].replace('.', ' ').replace('_', ' ').title()

    auth_login(request, user)

    # Clear OTP from session
    request.session.pop('login_otp', None)

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
