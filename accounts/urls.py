from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
   path('login/', views.LoginView.as_view(), name='login'),
   path('register/', views.RegisterView.as_view(), name='register'),
   path('profile/', views.ProfileView.as_view(), name='profile'),
   path('logout/', views.CustomLogoutView.as_view(next_page='menu:home'), name='logout'),
   path('address/add/', views.AddAddressView.as_view(), name='add_address'),
]