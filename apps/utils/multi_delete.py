from rest_framework import serializers


class MultiDeleteRequestSerializer(serializers.Serializer):
    list_id = serializers.ListField(child=serializers.IntegerField(), required=True)
    
    def create(self, validated_data):
        pass
    
    def update(self, instance, validated_data):
        pass
