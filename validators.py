from rest_framework import serializers
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

mobile_number_validator = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message="Mobile number must be entered in the format: '9999999999'. only 10 digits allowed."
)  

def validate_password(password):
    if not 8 <= len(password) <= 15:
        raise ValidationError(_('Password must be between 8 and 20 characters long.'), code='password_length')

    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    if not re.match(password_regex, password):
        raise ValidationError(_('Password must contain at least one lowercase letter, one uppercase letter, one number, and one special character.'), code='password_complexity')


class UserLoginValidator(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False, error_messages={
        'required': 'Email is required field',
        'null': 'email cannot be null',
        'blank': 'Email field cannot be empty'
    })
    password = serializers.CharField(max_length=20, required=True, allow_null=False, allow_blank=False, error_messages={
        'required': 'Password is required field',
        'null': 'password cannot be null',
        'blank': 'Password field cannot be empty'
    },validators=[validate_password])
    
    logged_device_id= serializers.CharField(required=False,allow_null=True, allow_blank=True)

class StaffLoginValidator(serializers.Serializer):
    mobile = serializers.CharField(required=True, allow_null=False, allow_blank=False, error_messages={
        'required':"mobile is required field",
        "null": "mobile cannot be null",
        "blank":"mobile field cannot be empty"
    })


class OTPValidator(serializers.Serializer):
    mobile = serializers.CharField(required=True, allow_null=False, allow_blank=False, error_messages={
        'required': 'Mobile Number is required field',
        'null': 'mobile cannot be null',
        'blank': 'Mobile Number field cannot be empty'
    }, validators=[mobile_number_validator])
    otp = serializers.CharField(required=True, allow_blank=False, min_length=6, max_length=6, error_messages = {
        'required': 'Otp is required',
        'blank': 'Otp cannot be empty',
        'min_length': 'Otp cannot be less than 6 digits',
        'max_length': 'Otp cannot be more than 6 digits',
    })

class VerifyPasswordValidator(serializers.Serializer):
    password = serializers.CharField(required=True, allow_blank=False, error_messages={
        'required': 'Password is required',
        'blank': 'Password cannot be empty',
    })

class ChangePasswordValidator(serializers.Serializer):
    password = serializers.CharField(required=True, allow_blank=False, error_messages={
        'required': 'Password is required',
        'blank': 'Password cannot be empty',
    })
    confirm_password = serializers.CharField(required=True, allow_blank=False, error_messages={
        'required': 'Password is required',
        'blank': 'Password cannot be empty',
    })

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Password and Confirm Password should be same")
        return attrs
    
class ProfileUpdateValidator(serializers.Serializer):
    full_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    image = serializers.ImageField(required=False, allow_empty_file=False)
