from .models import Category
from orders.models import Saved

def categories_processor(request):
    return {
        'categories': Category.objects.prefetch_related('subcategories').all(),
        'saved_count': Saved.objects.count()
    }
