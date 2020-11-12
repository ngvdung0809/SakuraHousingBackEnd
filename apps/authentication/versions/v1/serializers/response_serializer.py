from rest_framework import serializers

from SakuraHousing import settings
from apps.authentication.models import Accounts, Tenants


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'


class TenantResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenants
        fields = "__all__"
