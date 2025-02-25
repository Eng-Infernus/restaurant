# admin_dashboard/views.py
import csv
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.db.models import Sum, Count, Avg
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic import TemplateView, View
from accounts.models import User
from menu.models import FoodItem
from orders.models import Order


@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        context.update({
            'today_orders': Order.objects.filter(created_at__date=today).count(),
            'today_sales': Order.objects.filter(created_at__date=today).aggregate(Sum('total'))['total__sum'] or 0,
            'pending_orders': Order.objects.filter(status='pending').count(),
            'popular_items': FoodItem.objects.annotate(order_count=Count('orderitem')).order_by('-order_count')[:5]
        })

        return context


@method_decorator(staff_member_required, name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        context.update({
            'daily_sales': Order.objects.filter(created_at__date=today).aggregate(
                total=Sum('total'),
                count=Count('id')
            ),
            'pending_orders': Order.objects.filter(status='pending').count(),
            'recent_orders': Order.objects.order_by('-created_at')[:5],
            'low_stock_items': FoodItem.objects.filter(is_available=False)
        })
        return context


@method_decorator(staff_member_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'
    ordering = ['-created_at']


@method_decorator(staff_member_required, name='dispatch')
class ExportReportView(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Orders', 'Total Sales'])

        # Get last 30 days of sales
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)

        orders = Order.objects.filter(
            created_at__date__range=[start_date, end_date]
        ).values('created_at__date').annotate(
            total_sales=Sum('total'),
            order_count=Count('id')
        ).order_by('created_at__date')

        for order in orders:
            writer.writerow([
                order['created_at__date'],
                order['order_count'],
                order['total_sales']
            ])

        return response


@method_decorator(staff_member_required, name='dispatch')
class AnalyticsView(TemplateView):
    template_name = 'analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)

        # Sales analytics
        context['monthly_sales'] = Order.objects.filter(
            created_at__gte=thirty_days_ago
        ).aggregate(
            total_sales=Sum('total'),
            avg_order_value=Avg('total'),
            order_count=Count('id')
        )

        # Popular items
        context['popular_items'] = FoodItem.objects.annotate(
            total_orders=Count('orderitem')
        ).order_by('-total_orders')[:10]

        # Sales by payment method
        context['payment_methods'] = Order.objects.filter(
            created_at__gte=thirty_days_ago
        ).values('payment_method').annotate(
            count=Count('id'),
            total=Sum('total')
        )

        return context


@method_decorator(staff_member_required, name='dispatch')
class MenuItemListView(ListView):
    model = FoodItem
    template_name = 'menu/list.html'
    context_object_name = 'menu_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FoodItem.objects.values('category__name_en').annotate(
            item_count=Count('id')
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__id=category)
        return queryset.select_related('category')


@method_decorator(staff_member_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'users_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone_number__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = User.objects.count()
        context['active_users'] = User.objects.filter(is_active=True).count()
        return context
