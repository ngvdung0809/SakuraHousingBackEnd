from rest_framework import serializers

from apps.authentication.models import Accounts, Tenants
from apps.common.models import Districts
from apps.utils.constants import RoleType


class DistrictResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Districts
        fields = '__all__'


class TenantResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenants
        fields = ['id', 'name', 'address', 'description', 'phone', 'phone2', 'email', 'email2', 'dkkd', 'tax_code',
                  'rep', 'rep_role', 'ten_tk', 'so_TK', 'chi_nhanh', 'ngan_hang', 'ten_tk2', 'so_TK2', 'chi_nhanh2',
                  'ngan_hang2', 'note']


class UserResponseSerializer(serializers.ModelSerializer):
    tenant = TenantResponseSerializer()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Accounts
        fields = ('id', 'username', 'full_name', 'role', 'staff_code', 'tenant')

    def get_role(self, obj):
        if obj.role == RoleType.ADMIN.value:
            return 'Admin'
        elif obj.role == RoleType.VIEWER.value:
            return 'View'
        else:
            return 'Disable'
