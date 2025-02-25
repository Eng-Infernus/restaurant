# orders/views.py
import decimal
import uuid
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.generic import ListView, TemplateView, View

from menu.models import FoodItem
from .models import Order, OrderItem

User = get_user_model()


class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-created_at')


class CartView(TemplateView):
    template_name = 'orders/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        cart_items = []
        subtotal = Decimal('0.000')
        delivery_fee = Decimal('1.000')

        for item_id, quantity in cart.items():
            try:
                food_item = FoodItem.objects.get(id=item_id)
                total = food_item.price * quantity
                subtotal += total
                cart_items.append({
                    'food_item': food_item,
                    'quantity': quantity,
                    'total': total
                })
            except FoodItem.DoesNotExist:
                continue

        total = subtotal + delivery_fee

        context.update({
            'cart_items': cart_items,
            'subtotal': subtotal,
            'delivery_fee': delivery_fee,
            'total': total
        })
        return context


class AddToCartView(View):
    def post(self, request):
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))

        item = get_object_or_404(FoodItem, id=item_id, is_available=True)
        cart = request.session.get('cart', {})

        if str(item_id) in cart:
            cart[str(item_id)] += quantity
        else:
            cart[str(item_id)] = quantity

        request.session['cart'] = cart

        return JsonResponse({
            'success': True,
            'cart_total': sum(cart.values()),
            'message': 'Item added to cart'
        })


class UpdateCartView(View):
    def post(self, request):
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))

        if quantity < 1:
            return JsonResponse({
                'success': False,
                'message': 'Invalid quantity'
            }, status=400)

        cart = request.session.get('cart', {})
        if str(item_id) in cart:
            cart[str(item_id)] = quantity
            request.session['cart'] = cart

            return JsonResponse({
                'success': True,
                'cart_total': sum(cart.values()),
                'message': 'Cart updated'
            })
        return JsonResponse({
            'success': False,
            'message': 'Item not in cart'
        }, status=404)


class RemoveFromCartView(View):
    def post(self, request):
        item_id = request.POST.get('item_id')
        cart = request.session.get('cart', {})

        if str(item_id) in cart:
            del cart[str(item_id)]
            request.session['cart'] = cart

            return JsonResponse({
                'success': True,
                'cart_total': sum(cart.values()),
                'message': 'Item removed from cart'
            })
        return JsonResponse({
            'success': False,
            'message': 'Item not in cart'
        }, status=404)


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'orders/checkout.html'

    def get(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            messages.warning(request, _("Your cart is empty"))
            return redirect('orders:cart')

        cart_items = []
        subtotal = Decimal('0.000')
        delivery_fee = Decimal('1.000')

        for item_id, quantity in cart.items():
            try:
                food_item = FoodItem.objects.get(id=item_id)
                total = food_item.price * quantity
                subtotal += total
                cart_items.append({
                    'food_item': food_item,
                    'quantity': quantity,
                    'total': total
                })
            except FoodItem.DoesNotExist:
                continue

        total = subtotal + delivery_fee

        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'delivery_fee': delivery_fee,
            'total': total
        }
        return render(request, self.template_name, context)

    def post(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            messages.warning(request, _("Your cart is empty"))
            return redirect('orders:cart')

        # Get form data
        payment_method = request.POST.get('payment_method')
        saved_address_id = request.POST.get('saved_address')

        # Calculate totals
        subtotal = Decimal('0.000')
        delivery_fee = Decimal('1.000')
        items_json = []

        for item_id, quantity in cart.items():
            try:
                food_item = FoodItem.objects.get(id=item_id)
                total = food_item.price * quantity
                subtotal += total
                items_json.append({
                    'id': str(food_item.id),
                    'name': food_item.name_en,
                    'price': str(food_item.price),
                    'quantity': quantity,
                    'total': str(total)
                })
            except FoodItem.DoesNotExist:
                continue

        total = subtotal + delivery_fee

        # Get delivery address
        if saved_address_id:
            address = request.user.addresses.get(id=saved_address_id)
            delivery_address = f"{address.area}, Block {address.block}, Street {address.street}, Building {address.building}"
            if address.apartment:
                delivery_address += f", Apartment {address.apartment}"
        else:
            # Collect address from form
            area = request.POST.get('area')
            block = request.POST.get('block')
            street = request.POST.get('street')
            building = request.POST.get('building')
            apartment = request.POST.get('apartment', '')

            delivery_address = f"{area}, Block {block}, Street {street}, Building {building}"
            if apartment:
                delivery_address += f", Apartment {apartment}"

        # Create order
        order = Order.objects.create(
            order_number=uuid.uuid4(),
            customer=request.user,
            item=items_json,  # JSON field
            total=total,
            delivery_address=delivery_address,
            payment_method=payment_method,
            status='pending'
        )

        # Create order items
        for item_id, quantity in cart.items():
            try:
                food_item = FoodItem.objects.get(id=item_id)
                OrderItem.objects.create(
                    order=order,
                    food_item=food_item,
                    quantity=quantity,
                    price=food_item.price
                )
            except FoodItem.DoesNotExist:
                continue

        # Clear cart
        request.session['cart'] = {}
        messages.success(request, _("Your order has been placed successfully"))

        # Redirect to receipt page
        return redirect('orders:receipt', order_id=order.id)


class OrderReceiptView(LoginRequiredMixin, View):
    template_name = 'orders/receipt.html'

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
            order_items = order.items.all()

            context = {
                'order': order,
                'order_items': order_items,
                'delivery_fee': Decimal('1.000'),
                'subtotal': order.total - Decimal('1.000')
            }
            return render(request, self.template_name, context)
        except Order.DoesNotExist:
            messages.error(request, _("Order not found"))
            return redirect('orders:history')
