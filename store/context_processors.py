# store/context_processors.py
from .static_data import CATEGORIES

def global_store_context(request):
    return {
        'CATEGORIES': CATEGORIES,
    }
