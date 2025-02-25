# accounts/views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import UserRegisterForm, UserProfileForm, CustomAuthenticationForm
from .models import User, Address
from django.http import JsonResponse
from django.utils.translation import gettext as _


class CustomLogoutView(AuthLogoutView):
    next_page = 'menu:home'


class AddAddressView(LoginRequiredMixin, CreateView):
    model = Address
    fields = ['area', 'block', 'street', 'building', 'apartment', 'is_default']

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.is_default:
            self.request.user.addresses.update(is_default=False)
        self.object = form.save()
        return JsonResponse({'success': True})


# accounts/views.py
class LoginView(AuthLoginView):
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True


class LogoutView(AuthLogoutView):
    next_page = 'accounts:login'


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        # Ensure phone number is formatted correctly
        phone = form.cleaned_data.get('phone_number', '')
        print(form.cleaned_data)
        if phone and not phone.startswith('+965'):
            form.instance.phone_number = f"+965{phone}"
        messages.success(self.request, _("Profile updated successfully"))
        return super().form_valid(form)
