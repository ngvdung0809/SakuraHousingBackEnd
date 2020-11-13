from rest_framework import serializers

from apps.authentication.models import Accounts, Tenants


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ('id', 'username', 'full_name', 'role', 'staff_code', 'tenant')


class TenantResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenants
        fields = ['id', 'name', 'address', 'description', 'phone', 'phone2', 'email', 'email2', 'dkkd', 'tax_code',
                  'rep', 'rep_role', 'ten_tk', 'so_TK', 'chi_nhanh', 'ngan_hang', 'ten_tk2', 'so_TK2', 'chi_nhanh2',
                  'ngan_hang2', 'note']
