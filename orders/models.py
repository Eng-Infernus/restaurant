# orders/models.py
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from menu.models import FoodItem


class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    PAYMENT_METHODS = [
        ('knet', 'KNET'),
        ('cash', _('Cash on Delivery')),
    ]

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('preparing', _('Preparing')),
        ('ready', _('Ready for Delivery')),
        ('delivering', _('Out for Delivery')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]

    order_number = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    customer = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    item = models.JSONField()  # Stores order items with quantities and prices
    total = models.DecimalField(max_digits=8, decimal_places=3)
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHODS
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number}"


class Notification(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='order_notifications'
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='order_notifications'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.phone_number}"



class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=3)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.food_item.name_en}"