from django.contrib.auth.base_user import AbstractBaseUser
from authentication.models import CustomUser
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from django.core.exceptions import ValidationError

class AuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(Q(email=username) | Q(mobile=username))
            if user.user_type == "staff":
                if password:
                    if not user.otp == password:
                        raise ValidationError("otp did not match.")
                    user.save()
                return user
            if user.user_type == "super_admin":            
                if password:
                    if not user.check_password(password):
                        raise ValidationError("Password did not match.")
                    user.save()
                return user
        except CustomUser.DoesNotExist as e:
            raise ValidationError("No User Found with the given email.")
        
    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist as e:
            raise ValidationError("No User Found with the given email.")