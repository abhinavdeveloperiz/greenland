# store/views.py
from django.shortcuts import render
from django.http import Http404
from .static_data import (
    CATEGORIES, 
    PRODUCTS, 
    get_category_by_slug, 
    get_product_by_id, 
    get_products_by_category, 
    get_related_products
)

def home_view(request):
    featured_products = [p for p in PRODUCTS if p.get('isFeatured')]
    new_arrivals = PRODUCTS[:4]
    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': CATEGORIES,
    }
    return render(request, 'pages/home.html', context)

def products_view(request):
    search_query = request.GET.get('search', '').strip().lower()
    selected_category = request.GET.get('category', 'all')
    sort_by = request.GET.get('sort', 'featured')
    max_price = float(request.GET.get('max_price', 1000))
    availability = request.GET.get('availability', 'all')

    def matches_filters(p):
        if search_query and not any(search_query in p[field].lower() for field in ('name', 'description', 'categoryName')):
            return False
        if selected_category != 'all' and p['category'] != selected_category:
            return False
        if p['price'] > max_price:
            return False
        if availability != 'all' and p['availability'] != availability:
            return False
        return True

    filtered = [p for p in PRODUCTS if matches_filters(p)]

    # Sorting
    sort_keys = {
        'price_asc': lambda x: x['price'],
        'price_desc': lambda x: -x['price'],
        'name_asc': lambda x: x['name'],
        'featured': lambda x: -1 if x.get('isFeatured') else 0,
    }
    filtered.sort(key=sort_keys.get(sort_by, sort_keys['featured']))

    context = {
        'products': filtered,
        'search_query': search_query,
        'selected_category': selected_category,
        'sort_by': sort_by,
        'max_price': int(max_price),
        'availability': availability,
        'total_count': len(filtered),
    }
    return render(request, 'pages/products.html', context)

def category_view(request, slug):
    category = get_category_by_slug(slug)
    if not category:
        raise Http404("Category not found")
    
    category_products = get_products_by_category(slug)
    context = {
        'category': category,
        'products': category_products,
        'total_count': len(category_products)
    }
    return render(request, 'pages/category.html', context)

def categories_view(request):
    context = {
        'categories': CATEGORIES,
    }
    return render(request, 'pages/categories.html', context)

def about_view(request):
    return render(request, 'pages/about.html')

def contact_view(request):
    return render(request, 'pages/contact.html')

def product_detail_view(request, product_id):
    product = get_product_by_id(product_id)
    if not product:
        raise Http404("Product not found")
    
    context = {
        'product': product,
        'related_products': get_related_products(product, limit=4),
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
