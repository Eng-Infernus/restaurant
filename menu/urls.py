from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('menu/', views.MenuListView.as_view(), name='list'),
    path('menu/<int:pk>/', views.MenuDetailView.as_view(), name='detail'),
    path('menu/category/<slug:category_slug>/', views.CategoryMenuView.as_view(), name='category'),
]