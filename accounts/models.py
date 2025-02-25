# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )
    phone_regex = RegexValidator(
        regex=r'^\+965[0-9]{8}$',
        message=_(
            "Phone number must be entered in the format: '+96555555555'. Up to 8 digits allowed after country code.")
    )
    phone_number = models.CharField(
        _("Phone number"),
        validators=[phone_regex],
        max_length=12,  # +965 + 8 digits
        unique=True,
        help_text=_("Required. Format: +96555555555")
    )
    address = models.TextField(_("Address"))
    preferred_language = models.CharField(
        _("Preferred Language"),
        max_length=2,
        choices=[('ar', _('Arabic')), ('en', _('English'))],
        default='en'
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email']


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    area = models.CharField(max_length=100)
    block = models.CharField(max_length=10)
    street = models.CharField(max_length=100)
    building = models.CharField(max_length=50)
    apartment = models.CharField(max_length=50, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.area}, Block {self.block}, Street {self.street}"
