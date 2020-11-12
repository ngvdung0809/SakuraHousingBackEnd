from rest_framework import serializers

from SakuraHousing import settings
from apps.authentication.models import Accounts


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'
