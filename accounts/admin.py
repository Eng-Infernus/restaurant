from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address
from django.contrib.admin.forms import AdminAuthenticationForm


class UsernameAdminAuthenticationForm(AdminAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'


# Register User model with built-in UserAdmin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone_number',)}),
    )


# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Address)
admin.site.login_form = UsernameAdminAuthenticationForm
