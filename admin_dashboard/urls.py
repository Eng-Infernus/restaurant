# admin_dashboard/urls.py
from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
   path('', views.AdminDashboardView.as_view(), name='dashboard'),
   path('orders/', views.OrderListView.as_view(), name='orders'),
   path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
   path('users/', views.UserListView.as_view(), name='users'),
   path('menu-items/', views.MenuItemListView.as_view(), name='menu_items'),
   path('export-report/', views.ExportReportView.as_view(), name='export_report'),
]