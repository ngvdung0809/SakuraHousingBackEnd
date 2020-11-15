from rest_framework import serializers

from apps.contract.models import HDGroups, HDMoiGioi


class HDGroupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDGroups
        fields = [
            'id',
            'name',
            'can_ho',
        ]

    def create(self, validated_data):
        self.validated_data['created_by'] = self.context['request'].user
        self.validated_data['updated_by'] = self.context['request'].user
        hd_group = HDGroups.objects.create(**self.validated_data)
        return hd_group

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        for i in validated_data.keys():
            setattr(instance, i, validated_data[i])
        instance.save()
        return instance


class HDMoiGioiRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDMoiGioi
        fields = [
            'hd_group',
            'tenant',
            'tien_moi_gioi',
            'note'
        ]

    def create(self, validated_data):
        hd_moi_gioi = HDGroups.objects.create(**self.validated_data)
        return hd_moi_gioi

    def update(self, instance, validated_data):
        for i in validated_data.keys():
            setattr(instance, i, validated_data[i])
        instance.save()
        return instance
