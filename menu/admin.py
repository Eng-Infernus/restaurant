# menu/admin.py
from django.contrib import admin
from .models import Category, FoodItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_ar', 'slug']
    prepopulated_fields = {'slug': ('name_en',)}


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'category', 'price', 'is_available']
    list_filter = ['category', 'is_available', 'is_vegetarian']
    search_fields = ['name_en', 'name_ar']
