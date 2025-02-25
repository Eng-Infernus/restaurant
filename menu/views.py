# menu/views.py
from django.views.generic import ListView, DetailView
from .models import FoodItem, Category
from django.db.models import Q
from django.views.generic import TemplateView
from django.db.models import Count


class MenuListView(ListView):
    model = FoodItem
    template_name = 'menu/list.html'
    context_object_name = 'food_items'

    def get_queryset(self):
        queryset = FoodItem.objects.filter(is_available=True)
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class MenuDetailView(DetailView):
    model = FoodItem
    template_name = 'menu/detail.html'
    context_object_name = 'item'


class HomeView(TemplateView):
    template_name = 'menu/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use annotate() with Count() for proper aggregation
        context['popular_items'] = FoodItem.objects.filter(
            is_available=True
        ).annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:6]
        return context


class CategoryMenuView(ListView):
    model = FoodItem
    template_name = 'menu/list.html'
    context_object_name = 'food_items'

    def get_queryset(self):
        return FoodItem.objects.filter(
            category__slug=self.kwargs['category_slug'],
            is_available=True
        )
