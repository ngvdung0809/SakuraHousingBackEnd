from rest_framework import serializers

from SakuraHousing import settings
from apps.authentication.models import User


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'gender', 'birthday', 'is_active', 'is_admin', 'created_at']
        extra_kwargs = {
            'created_at': {'format': settings.DATE_TIME_FORMATS[0]},
        }
