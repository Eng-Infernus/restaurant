from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check if this is an admin login
        if request and request.path.startswith('/admin/'):
            try:
                # For admin, authenticate by username
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        else:
            # For regular users, authenticate by phone number
            try:
                user = User.objects.get(phone_number=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None