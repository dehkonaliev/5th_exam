from django.urls import path
from .views import SavedView, OrderedItemsView, delete_ordered_items

urlpatterns = [
    path('saved', SavedView.as_view(), name='saved'),
    path('ordered-items', OrderedItemsView.as_view(), name='order-success'),
    path('ordered-items/delete/<int:pk>', delete_ordered_items, name='delete-order')
]