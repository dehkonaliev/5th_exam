from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Saved, Order, OrderItem
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

@login_required
def add_saved(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    print(quantity)
    print(quantity)
    
    Saved.objects.create(
        user=user,
        product=product,
        quantity=quantity
    )
    
    return redirect('saved')


class HomeView(View):
    def get(self, request):
        latest_products = Product.objects.order_by('-id')[:6]
        return render(request, 'index.html', {'latest_products': latest_products})


class SavedView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        
        saved_items = Saved.objects.filter(user=user).order_by('-id')
        
        return render(request, 'orders/order-item.html', {'items':saved_items})
    
    def post(self, request):
        user = request.user
        items = request.POST.getlist('order-item')
        method = request.POST.get('method')
        saved_items = Saved.objects.filter(user=user).order_by('-id')
        
        if method == 'Buy':
            order = Order.objects.create(user=user, status='pending')
            for item in items:
                item = saved_items.filter(pk=item).first()
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.product.price
                )
                item.delete()
            
            return redirect('order-success')
        
        elif method == 'Delete':
            for item in items:
                item = saved_items.filter(pk=item).first()
                item.delete()
            
            return redirect('saved')

# @login_required
# def delete_saved(reuqest, pk):
#     if reuqest.method == "DELETE":
#         saved = get_object_or_404(Saved, pk=pk)
#         saved.delete()
#         return redirect('saved')
    
    
class OrderedItemsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        
        orders = Order.objects.filter(user=user).prefetch_related('items__product').order_by('-created_at')
        
        latest_order = orders.first()
        
        latest_order_total = 0
        if latest_order:
            latest_order_total = sum(
                item.quantity * item.price_at_purchase 
                for item in latest_order.items.all()
            )
            
        context = {
            'orders': orders,
            'latest_order': latest_order,
            'latest_order_total': latest_order_total
        }
        
        return render(request, 'orders/order-success.html', context)
    
@login_required
def cancel_ordered_items(request, pk):
    if request.method == "POST":
        saved = get_object_or_404(Order, pk=pk)
        
        saved.status = 'cancelled'
        saved.save()
        return redirect('order-success')
