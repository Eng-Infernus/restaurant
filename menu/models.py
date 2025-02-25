# menu/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name_en = models.CharField(_("Name (English)"), max_length=100)
    name_ar = models.CharField(_("Name (Arabic)"), max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name_en


class FoodItem(models.Model):
    SPICE_LEVELS = [
        (1, _("Mild")),
        (2, _("Medium")),
        (3, _("Hot")),
        (4, _("Extra Hot")),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name_en = models.CharField(_("Name (English)"), max_length=200)
    name_ar = models.CharField(_("Name (Arabic)"), max_length=200)
    description_en = models.TextField(_("Description (English)"))
    description_ar = models.TextField(_("Description (Arabic)"))
    price = models.DecimalField(max_digits=6, decimal_places=3)  # Kuwait uses 3 decimal places
    image = models.ImageField(upload_to='menu_items/')
    spice_level = models.IntegerField(choices=SPICE_LEVELS, default=1)
    is_available = models.BooleanField(default=True)
    is_vegetarian = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_en