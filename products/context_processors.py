from .models import Category
from orders.models import Saved

def categories_processor(request):
    # Fetch categories once, regardless of auth status
    context = {
        'categories': Category.objects.prefetch_related('subcategories').all()
    }
    
    # Strictly check if the user is logged in
    if request.user.is_authenticated:
        context['saved_count'] = Saved.objects.filter(user=request.user).count()
        
    return context
