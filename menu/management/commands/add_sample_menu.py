from django.core.management.base import BaseCommand
from menu.models import Category, FoodItem
from django.core.files.base import ContentFile
import requests


class Command(BaseCommand):
    help = 'Adds sample menu items'

    def handle(self, *args, **kwargs):
        # Create categories
        main_course, _ = Category.objects.get_or_create(
            slug="main-course",
            defaults={
                "name_en": "Main Course",
                "name_ar": "الطبق الرئيسي"
            }
        )

        appetizers, _ = Category.objects.get_or_create(
            slug="appetizers",
            defaults={
                "name_en": "Appetizers",
                "name_ar": "المقبلات"
            }
        )

        # Food items with image URLs
        FoodItem.objects.create(
            category=main_course,
            name_en="Machboos Chicken",
            name_ar="مجبوس دجاج",
            description_en="Traditional Kuwaiti spiced rice with chicken",
            description_ar="أرز كويتي تقليدي مع الدجاج",
            price=4.500,
            spice_level=2,
            is_available=True,
            image="https://www.endofthefork.com/wp-content/uploads/2023/06/machboos-sq.jpg"
        )

        FoodItem.objects.create(
            category=main_course,
            name_en="Mutabbaq",
            name_ar="مطبق",
            description_en="Stuffed meat pastry",
            description_ar="معجنات محشوة باللحم",
            price=3.750,
            spice_level=1,
            is_available=True,
            image="https://i.ytimg.com/vi/z51TV-7WTGo/maxresdefault.jpg"
        )

        FoodItem.objects.create(
            category=appetizers,
            name_en="Hummus",
            name_ar="حمص",
            description_en="Creamy chickpea dip with olive oil",
            description_ar="حمص كريمي مع زيت الزيتون",
            price=1.500,
            spice_level=0,
            is_vegetarian=True,
            is_available=True,
            image="https://terianncarty.com/wp-content/uploads/2023/04/CREAMY-CHICKPEA-HUMMUS-500x500.jpeg"
        )

        FoodItem.objects.create(
            category=appetizers,
            name_en="Fattoush",
            name_ar="فتوش",
            description_en="Fresh vegetable salad with toasted pita bread",
            description_ar="سلطة خضار طازجة مع خبز محمص",
            price=2.000,
            spice_level=0,
            is_vegetarian=True,
            is_available=True,
            image="https://i0.wp.com/walkingthroughlavenderfields.com/wp-content/uploads/2022/10/fattoush-01.jpeg?fit"
                  "=1280%2C854&ssl=1"
        )

        self.stdout.write(self.style.SUCCESS('Successfully added sample menu items'))