from django.urls import path
from .views import SavedView

urlpatterns = [
    path('saved', SavedView.as_view(), name='saved')
]