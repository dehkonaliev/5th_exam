from django.urls import path
from .views import SavedView, OrderedItemsView, cancel_ordered_items, add_saved, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('saved', SavedView.as_view(), name='saved'),
    path('orders/ordered-items', OrderedItemsView.as_view(), name='order-success'),
    path('orders/ordered-items/cancel/<int:pk>', cancel_ordered_items, name='delete-order'),
    path('orders/saved/add/<int:pk>', add_saved, name='add-saved')
]