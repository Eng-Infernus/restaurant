# admin_dashboard/models.py
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class DailySalesReport(models.Model):
    date = models.DateField(unique=True)
    total_sales = models.DecimalField(max_digits=10, decimal_places=3)
    total_orders = models.IntegerField()
    average_order_value = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    @classmethod
    def generate_report(cls, date=None):
        from orders.models import Order

        if date is None:
            date = timezone.now().date()

        orders = Order.objects.filter(
            created_at__date=date,
            status__in=['delivered', 'completed']
        )

        total_sales = orders.aggregate(Sum('total'))['total__sum'] or 0
        total_orders = orders.count()
        avg_order = total_sales / total_orders if total_orders > 0 else 0

        report, _ = cls.objects.update_or_create(
            date=date,
            defaults={
                'total_sales': total_sales,
                'total_orders': total_orders,
                'average_order_value': avg_order
            }
        )
        return report
