from django.urls import path
from .views import (
    CategoryListView,
    SubcategoryListView,
    ProductListView,
    ProductDetailView,
    ReviewCreateView,
    delete_review)

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('category/<int:category_id>/', SubcategoryListView.as_view(), name='subcategory-list'),
    path('subcategory/<int:subcategory_id>/', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/review/', ReviewCreateView.as_view(), name='review-create'),
    path('review/delete/<int:pk>', delete_review, name='delete-review')
]