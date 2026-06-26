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
        saved_items = Saved.objects.filter(user=user)
        items = request.POST.getlist('order-item')
        saved_items = Saved.objects.filter(user=user)
        order = Order.objects.create(user=user, status='pending')
        for item in items:
            item = saved_items.filter(pk=item)
            print(item.id)
            # OrderItem.objects.create(
            #     order=order,
            #     product=item.product,
            #     quantity=item.quantity,
            #     price_at_purchase=item.product.price
            # )
            
        # items.delete()
        
        return redirect('order-success')
    
class OrderedItemsView(View):
    def get(self, request):
        return render(request, 'orders/order-success.html')
