# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
   path('cart/', views.CartView.as_view(), name='cart'),
   path('checkout/', views.CheckoutView.as_view(), name='checkout'),
   path('history/', views.OrderHistoryView.as_view(), name='history'),
   path('add-to-cart/', views.AddToCartView.as_view(), name='add_to_cart'),
   path('update-cart/', views.UpdateCartView.as_view(), name='update_cart'),
   path('remove-from-cart/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
   path('receipt/<int:order_id>/', views.OrderReceiptView.as_view(), name='receipt'),
]