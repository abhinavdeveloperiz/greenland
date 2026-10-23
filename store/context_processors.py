# store/context_processors.py - Dynamic database context processor
from .models import Category, Brand
from .static_data import CATEGORIES as STATIC_CATEGORIES, BRANDS as STATIC_BRANDS

def global_store_context(request):
    """Global context processor providing categories and brands dynamically from the database."""
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

    return {
        'CATEGORIES': categories,
        'GLOBAL_BRANDS': brands,
    }
