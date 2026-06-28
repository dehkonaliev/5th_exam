from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Subcategory, Product, Review
from .forms import ReviewForm
from django.db.models import Q


class ProductListView(View):
    """Bitta subkategoriyaga tegishli productlarni ko'rsatadi"""
    def get(self, request, subcategory_id):
        subcategory = get_object_or_404(Subcategory, id=subcategory_id)
        products = subcategory.products.filter(is_active=True).order_by('-id')
        return render(request, 'products/product-list.html', {
            'subcategory': subcategory,
            'products': products,
        })
        
        
class SupProductListView(View):
    """Bitta subkategoriyaga tegishli productlarni ko'rsatadi"""
    def get(self, request, pk):
        products = Product.objects.filter(subcategory__category=pk).order_by('-id')
        category = get_object_or_404(Category, pk=pk)
        return render(request, 'products/sup-product-list.html', {
            'products': products,
            'category': category
        })


class ProductDetailView(View):
    """Product haqida to'liq ma'lumot + reviewlar + review qo'shish formasi"""
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        reviews = product.reviews.all()
        form = ReviewForm()
        reviewed = request.user in [review.user for review in reviews]
        user_review_pk = False
        if reviewed:
            user_review_pk = [review.pk for review in reviews if review.user == request.user ][0]
        print(user_review_pk)
        
        return render(request, 'products/product-detail.html', {
            'product': product,
            'reviews': reviews,
            'user_reviewed':reviewed,
            'user_review_pk': user_review_pk,
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
    
    
@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    next_page = request.META.get('HTTP_REFERER')
        
    if next_page:
        return redirect(next_page)
    
    return redirect('home')


class CategoriesView(View):
    def get(self, request):
        products = Product.objects.all().order_by('-id')[:20]
        return render(request, 'products/categories.html', {'products': products})
    
        
    
def search(request):
    
    query = request.POST.get('search_query')
        
    products = Product.objects.filter(Q(name__icontains=query)  | Q(desc__icontains=query))
    
    return render(request, 'products/search.html', {'products': products, 'search_query':query})
    
        
        