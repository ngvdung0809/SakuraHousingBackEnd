from django.utils import timezone
from rest_framework import serializers

from apps.payment.models import PaymentTransactions, ServiceTransactions
from apps.payment.utils.send_email import EmailTemplate
from apps.utils.constants import PaymentStatus
from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException


class PaymentHDRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    
    class Meta:
        model = PaymentTransactions
        fields = ['id']
    
    def validate(self, attrs):
        try:
            instance = PaymentTransactions.objects.get(pk=attrs['id'])
            return instance
        except PaymentTransactions.DoesNotExist:
            raise CustomException(ErrorCode.not_found_record)
    
    def save(self, **kwargs):
        instance = self.validated_data
        instance.status = PaymentStatus.PAID.value
        instance.ngay_thanh_toan_tt = timezone.now().date()
        instance.save()
        return instance


class PaymentServiceRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    
    class Meta:
        model = ServiceTransactions
        fields = ['id', 'so_tien']
    
    def validate(self, attrs):
        try:
            instance = ServiceTransactions.objects.get(pk=attrs['id'])
            return {'instance': instance, 'so_tien': attrs['so_tien']}
        except ServiceTransactions.DoesNotExist:
            raise CustomException(ErrorCode.not_found_record)
    
    def save(self, **kwargs):
        instance = self.validated_data['instance']
        instance.status = PaymentStatus.PAID.value
        instance.ngay_thanh_toan_tt = timezone.now().date()
        instance.so_tien = self.validated_data['so_tien']
        instance.save()
        return instance


class PaymentEmailRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    type_email = serializers.IntegerField(required=True, min_value=1, max_value=2)
    
    class Meta:
        model = PaymentTransactions
        fields = ['id', 'type_email']
    
    def validate(self, attrs):
        try:
            instance = PaymentTransactions.objects.prefetch_related('nguoi_gui', 'hop_dong').get(pk=attrs['id'])
            return {'instance': instance, 'type_email': attrs['type_email']}
        except PaymentTransactions.DoesNotExist:
            raise CustomException(ErrorCode.not_found_record)
    
    def save(self, **kwargs):
        send_mail = EmailTemplate()
        send_mail.send_payment_email(self.validated_data['instance'], self.validated_data['type_email'])
        return self.validated_data
