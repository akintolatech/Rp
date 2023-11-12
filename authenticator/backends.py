# myapp/backends.py
from django.contrib.auth.backends import BaseBackend
from .models import CustomUser


class MyAuthBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, ):
        try:
            user = CustomUser.objects.get(username=username)
            if user.password == password:
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
