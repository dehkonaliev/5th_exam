from django.shortcuts import render, redirect
from django.views import View
from .models import Saved, Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin


class SavedView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        
        saved_items = Saved.objects.filter(user=user)
        
        return render(request, 'orders/order-item.html', {'items':saved_items})
    

