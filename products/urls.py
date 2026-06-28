from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ReviewCreateView,
    CategoriesView,
    SupProductListView,
    search,
    
    delete_review)

urlpatterns = [
    path('subcategory/<int:subcategory_id>/', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/review/', ReviewCreateView.as_view(), name='review-create'),
    path('review/delete/<int:pk>', delete_review, name='delete-review'),
    path('categories', CategoriesView.as_view(), name='categories'), 
    path('category/<int:pk>', SupProductListView.as_view(), name='category-view'),
    path('search', search, name='search')
]