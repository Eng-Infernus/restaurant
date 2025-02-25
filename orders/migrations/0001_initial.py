# Generated by Django 5.0.2 on 2025-02-12 21:15

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('item', models.JSONField()),
                ('total', models.DecimalField(decimal_places=3, max_digits=8)),
                ('payment_method', models.CharField(choices=[('knet', 'KNET'), ('cash', 'Cash on Delivery')], max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('preparing', 'Preparing'), ('ready', 'Ready for Delivery'), ('delivering', 'Out for Delivery'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('delivery_address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_notifications', to='accounts.user')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_notifications', to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('food_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.fooditem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
            ],
        ),
    ]
