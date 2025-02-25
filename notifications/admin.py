# notifications/admin.py
from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__phone_number', 'order__order_number']
