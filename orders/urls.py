from django.urls import path
from .views import SavedView, OrderedItemsView

urlpatterns = [
    path('saved', SavedView.as_view(), name='saved'),
    path('ordered-items', OrderedItemsView.as_view(), name='order-success')
]