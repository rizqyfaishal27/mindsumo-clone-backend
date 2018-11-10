from django.contrib.auth.hashers import check_password
from .models import CustomUser

from .serializers import CustomUserSerializer

class CustomAuthBackend:

    def authenticate(self, request, email=None, password=None):
        try:
            user_to_login = CustomUser.objects.get(email=email)
            is_password_valid = check_password(password, user_to_login.password)
            if is_password_valid:
                return user_to_login
            else:
                return None
        except CustomUser.DoesNotExist:
            return None

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': CustomUserSerializer(user, context={'request': request}).data
    }