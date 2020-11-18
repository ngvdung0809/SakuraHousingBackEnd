import re

from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.authentication.models import Accounts, Tenants
from apps.utils.config import PasswordRegex
from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException


class EmptySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class AccountCreateSerializer(serializers.ModelSerializer):
    staff_code = serializers.CharField(min_length=4, required=False)

    class Meta:
        model = Accounts
        fields = ('username', 'password', 'full_name', 'role', 'staff_code', 'tenant')
        extra_kwargs = {
            'staff_code': {'required': False},
        }

    def validate_password(self, value):
        if not re.search(PasswordRegex.password_regex, value):
            raise CustomException(ErrorCode.password_invalid)
        return value

    def create(self, validated_data):
        user = Accounts(
            username=validated_data.get('username'),
            full_name=validated_data.get('full_name'),
            staff_code=validated_data.get('staff_code', None),
            role=validated_data.get('role'),
            tenant=validated_data.get('tenant'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
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


class TenantRequestSerializer(serializers.ModelSerializer):
    phone2 = serializers.CharField(required=False)
    email2 = serializers.CharField(required=False)
    ten_tk2 = serializers.CharField(required=False)
    so_TK2 = serializers.CharField(required=False)
    chi_nhanh2 = serializers.CharField(required=False)
    ngan_hang2 = serializers.CharField(required=False)
    note = serializers.CharField(required=False)

    class Meta:
        model = Tenants
        fields = ['name', 'address', 'description', 'phone', 'phone2', 'email', 'email2', 'dkkd', 'tax_code', 'rep',
                  'rep_role', 'ten_tk', 'so_TK', 'chi_nhanh', 'ngan_hang', 'ten_tk2', 'so_TK2', 'chi_nhanh2',
                  'ngan_hang2', 'note']

    def create(self, validated_data):
        tenant = Tenants.objects.create(**self.validated_data)
        return tenant

    def update(self, instance, validated_data):
        for i in validated_data.keys():
            setattr(instance, i, validated_data[i])
        instance.save()
        return instance


class AccountRequestSerializer(serializers.ModelSerializer):
    staff_code = serializers.CharField(min_length=4, required=False)

    class Meta:
        model = Accounts
        fields = ('full_name', 'role', 'staff_code', 'tenant')

    def update(self, instance, validated_data):
        for i in validated_data.keys():
            setattr(instance, i, validated_data[i])
        instance.save()
        return instance
