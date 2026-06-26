from django.shortcuts import render, redirect
from django.views import View
from .models import Saved, Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin


class SavedView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        
        saved_items = Saved.objects.filter(user=user)
        
        return render(request, 'orders/order-item.html', {'items':saved_items})
    
    def post(self, request):
        user = request.user
        items = request.POST.getlist('order-item')
        saved_items = Saved.objects.filter(user=user)
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
