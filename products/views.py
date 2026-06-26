from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Category, Subcategory, Product, Review
from .forms import ReviewForm


class CategoryListView(View):
    """Barcha kategoriyalarni ko'rsatadi"""
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'products/category-list.html', {'categories': categories})


class SubcategoryListView(View):
    """Bitta kategoriyaga tegishli subkategoriyalarni ko'rsatadi"""
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        subcategories = category.subcategories.all()
        return render(request, 'products/subcategory-list.html', {
            'category': category,
            'subcategories': subcategories,
        })


class ProductListView(View):
    """Bitta subkategoriyaga tegishli productlarni ko'rsatadi"""
    def get(self, request, subcategory_id):
        subcategory = get_object_or_404(Subcategory, id=subcategory_id)
        products = subcategory.products.filter(is_active=True)
        return render(request, 'products/product-list.html', {
            'subcategory': subcategory,
            'products': products,
        })


class ProductDetailView(View):
    """Product haqida to'liq ma'lumot + reviewlar + review qo'shish formasi"""
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        reviews = product.reviews.all()
        form = ReviewForm()
        return render(request, 'products/product-detail.html', {
            'product': product,
            'reviews': reviews,
            'form': form,
        })


class ReviewCreateView(LoginRequiredMixin, View):
    """Productga review qo'shish (faqat login qilgan user)"""
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Sharhingiz qo'shildi.")
        else:
            messages.error(request, "Sharh qo'shishda xatolik yuz berdi.")
        return redirect('product-detail', pk=product.pk)
