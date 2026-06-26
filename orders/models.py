from django.db import models
from products.models import Product
from users.models import CustomUser

class Saved(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

class Order(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('shipped' ,'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
    def get_total_price(self):
        return sum(item.quantity * item.price_at_purchase for item in self.items.all())

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product} - {self.order.id}"
    
    def get_subtotal(self):
        """Calculates the subtotal for this specific order item."""
        return self.quantity * self.price_at_purchase
    


    