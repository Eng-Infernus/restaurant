# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm
from .models import User, Address
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'preferred_language']


# accounts/forms.py
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['area', 'block', 'street', 'building', 'apartment', 'is_default']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_('Username or Phone Number'))

    class Meta:
        fields = ['username', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'preferred_language']

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        print(self.cleaned_data)
        if not phone.startswith('+965'):
            phone = f"+965{phone}"
        return phone