from django.db import models

# Create your models here.
from django.db import models

from django.db import models
from django.contrib.postgres.fields import JSONField  

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

  
    image_thumbnail = models.ImageField(upload_to='products/thumbnails/', null=True, blank=True)
    image_mobile = models.ImageField(upload_to='products/mobile/', null=True, blank=True)
    image_tablet = models.ImageField(upload_to='products/tablet/', null=True, blank=True)
    image_desktop = models.ImageField(upload_to='products/desktop/', null=True, blank=True)

    
    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    status = models.CharField(max_length=20, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.unit_price

