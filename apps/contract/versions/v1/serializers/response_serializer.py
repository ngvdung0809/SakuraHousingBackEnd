from rest_framework import serializers

from apps.common.versions.v1.serializers.response_serializer import CanHoResponseSerializer
from apps.contract.models import HDGroups


class HDGroupResponseSerializer(serializers.ModelSerializer):
    can_ho = CanHoResponseSerializer()

    class Meta:
        model = HDGroups
        fields = [
            'id',
            'name',
            'can_ho',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]
