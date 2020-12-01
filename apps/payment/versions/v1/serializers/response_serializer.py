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
            'can_ho',
            'hop_dong_type',
            'dot_thanh_toan',
            'start_date',
            'end_date',
            'status',
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
    
    def get_nguoi_gui(self, obj):
        return obj.nguoi_gui.name
    
    def get_nguoi_nhan(self, obj):
        return obj.nguoi_nhan.name


class ServiceTransactionResponseSerializer(serializers.ModelSerializer):
    can_ho = serializers.SerializerMethodField()
    dich_vu = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceTransactions
        fields = [
            'id',
            'can_ho',
            'dich_vu',
            'dot_thanh_toan',
            'so_tien',
            'ngay_thanh_toan_du_kien',
            'ngay_thanh_toan_tt',
            'status',
            'note',
        ]
    
    def get_dich_vu(self, obj):
        return obj.hd_2_dichvu.dich_vu.name
    
    def get_can_ho(self, obj):
        return obj.hd_2_dichvu.hd_thue.hd_group.can_ho.name
