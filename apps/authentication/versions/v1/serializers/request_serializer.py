from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers

from apps.authentication.models import Accounts
import re
from datetime import datetime, date
from django.conf import settings

from apps.utils.config import PasswordRegex
from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException


class EmptySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass
    
    def create(self, validated_data):
        pass


# class UserCreateSerializer(serializers.ModelSerializer):
#     birthday = serializers.CharField(required=True, max_length=255)
#     company_code = serializers.CharField(max_length=4, min_length=4, required=False)
#     email = serializers.EmailField(required=True, max_length=255)
#
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'username', 'gender', 'birthday', 'company_code')
#         extra_kwargs = {
#             'company_code': {'required': False},
#             'birthday': {'input_formats': settings.DATE_FORMATS},
#         }
#
#     def validate_birthday(self, value):
#         try:
#             current_date = date.today()
#             birthday_user = datetime.strptime(value, settings.DATE_FORMATS[0])
#         except Exception as e:
#             raise CustomException(ErrorCode.birthday_invalid_format)
#         if birthday_user.date() > current_date:
#             raise CustomException(ErrorCode.birthday_invalid_date)
#         return birthday_user.date()
#
#     def validate_password(self, value):
#         if not re.search(PasswordRegex.password_regex, value):
#             raise CustomException(ErrorCode.password_invalid)
#         return value
#
#     def create(self, validated_data):
#         try:
#             user = User.objects.filter(email=validated_data.get('email')).get()
#             if user.is_active:
#                 raise CustomException(ErrorCode.account_has_exist)
#         except User.DoesNotExist:
#             user = User(
#                 email=validated_data.get('email'),
#                 username=validated_data.get('username'),
#                 gender=validated_data.get('gender'),
#                 birthday=validated_data.get('birthday'),
#                 company=validated_data.get('company', None),
#             )
#             user.set_password(validated_data.get('password'))
#             user.save()
#         return user
#

class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    
    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise CustomException(ErrorCode.login_fail)
        return user
    
    def create(self, validated_data):
        pass
    
    def update(self, instance, validated_data):
        pass
#
#
# class CheckEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True, max_length=255)
#
#     def validate(self, attrs):
#         if User.objects.filter(email=attrs['email']).exists():
#             raise CustomException(ErrorCode.has_exist_email)
#         return attrs
#
#     def create(self, validated_data):
#         pass
#
#     def update(self, instance, validated_data):
#         pass
#
#
# class CheckCompanySerializer(serializers.Serializer):
#     company_code = serializers.CharField(max_length=4, min_length=4)
#
#     def validate(self, attrs):
#         if not Company.objects.filter(company_code=attrs['company_code']).exists():
#             raise CustomException(ErrorCode.not_found_company)
#         return attrs
#
#     def create(self, validated_data):
#         pass
#
#     def update(self, instance, validated_data):
#         pass
#
#
# class CheckOTPCodeSerializer(serializers.Serializer):
#     user = serializers.IntegerField(required=True)
#     otp_code = serializers.CharField(max_length=6, required=True)
#
#     def validate(self, attrs):
#         try:
#             user_code = UserAuth.objects.filter(
#                 user_id=attrs['user'],
#                 auth_code=attrs['otp_code']
#             ).get()
#             # check time code
#             if not user_code.created_at >= timezone.now() - relativedelta(minutes=3):
#                 raise CustomException(ErrorCode.otp_code_has_expired)
#             return user_code.user
#         except UserAuth.DoesNotExist:
#             raise CustomException(ErrorCode.wrong_data)
#
#     def save(self, **kwargs):
#         user = self.validated_data
#         user.is_active = True
#         user.save()
#         # delete otp code
#         UserAuth.objects.filter(user=user).delete()
#         return user
