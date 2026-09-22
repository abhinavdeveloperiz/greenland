# store/views.py
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
from .models import Category, Product, AdvertisementBanner, Brand

def home_view(request):
    categories = Category.objects.all().order_by('order', 'name')
    featured_products = Product.objects.filter(is_featured=True, is_active=True).select_related('category').prefetch_related('gallery_images')
    new_arrivals = Product.objects.filter(is_active=True).select_related('category').prefetch_related('gallery_images').order_by('-is_new', '-created_at')[:4]
    advertisement_banner = AdvertisementBanner.objects.filter(is_active=True).first()
    brands = Brand.objects.filter(is_active=True).order_by('order')

    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'brands': brands,
        'advertisement_banner': advertisement_banner,
    }
    return render(request, 'pages/home.html', context)

def products_view(request):
    search_query = request.GET.get('search', '').strip()
    selected_category = request.GET.get('category', 'all')
    selected_brand = request.GET.get('brand', 'all')
    sort_by = request.GET.get('sort', 'featured')
    
    try:
        max_price = float(request.GET.get('max_price', 15))
    except (ValueError, TypeError):
        max_price = 15.0

    availability = request.GET.get('availability', 'all')

    qs = Product.objects.filter(is_active=True).select_related('category').prefetch_related('gallery_images')

    if search_query:
        qs = qs.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    if selected_category != 'all':
        qs = qs.filter(category__slug=selected_category)

    if selected_brand != 'all':
        qs = qs.filter(brand_code=selected_brand)

    qs = qs.filter(price__lte=max_price)

    if availability != 'all':
        qs = qs.filter(availability=availability)

    # Sorting
    if sort_by == 'price_asc':
        qs = qs.order_by('price')
    elif sort_by == 'price_desc':
        qs = qs.order_by('-price')
    elif sort_by == 'name_asc':
        qs = qs.order_by('name')
    else: # featured
        qs = qs.order_by('-is_featured', '-is_new', '-created_at')

    # Brand counts across all active products
    brand_counts = {
        'all': Product.objects.filter(is_active=True).count(),
        'greenland': Product.objects.filter(is_active=True, brand_code='greenland').count(),
        '88': Product.objects.filter(is_active=True, brand_code='88').count(),
        '777': Product.objects.filter(is_active=True, brand_code='777').count(),
    }

    active_brand_obj = Brand.objects.filter(code=selected_brand, is_active=True).first() if selected_brand != 'all' else None
    active_category_obj = Category.objects.filter(slug=selected_category).first() if selected_category != 'all' else None

    # Categories with count of active products
    from django.db.models import Count
    categories_with_counts = Category.objects.annotate(
        active_count=Count('products', filter=Q(products__is_active=True))
    ).order_by('order', 'name')

    context = {
        'products': qs,
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'active_brand_obj': active_brand_obj,
        'active_category_obj': active_category_obj,
        'brand_counts': brand_counts,
        'categories_with_counts': categories_with_counts,
        'brands': Brand.objects.filter(is_active=True).order_by('order'),
        'sort_by': sort_by,
        'max_price': max_price,
        'availability': availability,
        'total_count': qs.count(),
    }
    return render(request, 'pages/products.html', context)

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category_products = category.products.filter(is_active=True).select_related('category').prefetch_related('gallery_images')
    
    context = {
        'category': category,
        'products': category_products,
        'total_count': category_products.count()
    }
    return render(request, 'pages/category.html', context)

def about_view(request):
    return render(request, 'pages/about.html')

def contact_view(request):
    return render(request, 'pages/contact.html')

def product_detail_view(request, product_id):
    product = get_object_or_404(Product.objects.select_related('category').prefetch_related('gallery_images'), id=product_id)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id).select_related('category')[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'pages/product_detail.html', context)

def cart_view(request):
    return render(request, 'pages/cart.html')

def checkout_view(request):
    return render(request, 'pages/checkout.html')

def order_confirmation_view(request, order_id):
    context = {'order_id': order_id}
    return render(request, 'pages/order_confirmation.html', context)

def order_tracking_view(request, order_id):
    context = {'order_id': order_id}
    return render(request, 'pages/order_tracking.html', context)

def order_history_view(request):
    return render(request, 'pages/order_history.html')

def wishlist_view(request):
    return render(request, 'pages/wishlist.html')

def profile_view(request):
    return render(request, 'pages/profile.html')

def login_view(request):
    return render(request, 'pages/login.html')

def register_view(request):
    return render(request, 'pages/register.html')
