from rest_framework import serializers

from SakuraHousing import settings
from apps.payment.models import PaymentTransactions, ServiceTransactions


class PaymentTransactionResponseSerializer(serializers.ModelSerializer):
    can_ho = serializers.SerializerMethodField()
    hop_dong_type = serializers.SerializerMethodField()
    nguoi_gui = serializers.SerializerMethodField()
    nguoi_nhan = serializers.SerializerMethodField()

    class Meta:
        model = PaymentTransactions
        fields = [
            'id',
            'can_ho'
            'hop_dong_type',
            'dot_thanh_toan',
            'start_date',
            'end_date',
            'status',  # choice
            'ngay_thanh_toan_du_kien',
            'ngay_thanh_toan_tt',
            'so_tien',
            'nguoi_gui',
            'nguoi_nhan',
        ]

    def get_can_ho(self, obj):
        return obj.hop_dong.hd_group.can_ho.name

    def get_hop_dong_type(self, obj):
        return obj.hop_dong.type_contract


class ServiceTransactionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTransactions
        fields = [
            'id',
            'hd_2_dichvu',
            'dot_thanh_toan',
            'so_tien',
            'ngay_thanh_toan_du_kien',
            'ngay_thanh_toan_tt',
            'status',  # choice
            'note',
        ]


class UnpaidResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransactions
        fields = [
            'id',
            'hop_dong',
            'dot_thanh_toan',
            'start_date',
            'end_date',
            'status',  # choice
            'ngay_thanh_toan_du_kien',
            'so_tien',
            'nguoi_gui',
            'nguoi_nhan',
        ]


class UnpaidServiceResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTransactions
        fields = [
            'id',
            'hd_2_dichvu',
            'dot_thanh_toan',
            'so_tien',
            'ngay_thanh_toan_du_kien',
            'status',  # choice
            'note',
        ]
