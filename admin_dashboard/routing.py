# admin_dashboard/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/admin_notifications/$', consumers.OrderNotificationConsumer.as_asgi()),
]

