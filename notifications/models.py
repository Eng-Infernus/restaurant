# notifications/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='system_notifications'
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='system_notifications'
    )

    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.phone_number}"