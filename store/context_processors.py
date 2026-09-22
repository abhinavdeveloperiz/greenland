# store/context_processors.py
from .models import Category
from .static_data import CATEGORIES as STATIC_CATEGORIES

def global_store_context(request):
    try:
        categories = list(Category.objects.all().order_by('order', 'name'))
        if not categories:
            categories = STATIC_CATEGORIES
    except Exception:
        categories = STATIC_CATEGORIES

    return {
        'CATEGORIES': categories,
    }
