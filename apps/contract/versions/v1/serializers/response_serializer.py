from rest_framework import serializers

from apps.authentication.versions.v1.serializers.response_serializer import TenantResponseSerializer
from apps.common.versions.v1.serializers.response_serializer import CanHoResponseSerializer, \
    KhachThueResponseSerializer, DichVuResponseSerializer
from apps.contract.models import HDGroups, HDThue, HDMoiGioi, HDDichVu, HD2DichVus


class HD2DichVusResponseSerializer(serializers.ModelSerializer):
    dich_vu = DichVuResponseSerializer()
    
    class Meta:
        model = HD2DichVus
        fields = [
            'id',
            'dich_vu',
            'ky_tt',
            'dinh_muc',
            'note',
        ]


class HDThueResponseSerializer(serializers.ModelSerializer):
    khach_thue = KhachThueResponseSerializer()
    
    class Meta:
        model = HDThue
        fields = [
            'id',
            'khach_thue',
            'start_date',
            'end_date',
            'dk_gia_han',
            'gia_thue_per_month',
            'gia_thue_per_month_nt',
            'ky_tt',
            'tien_dat_coc',
            'tien_dat_coc_nt',
            'note',
            'ngoai_te',
            'ty_gia',
            'ngay_lay_ti_gia',
            'ngay_ki',
            'ngay_nhan',
            'ngay_tra',
            'type_contract',
        ]


class SubHDThueResponseSerializer(HDThueResponseSerializer):
    services = serializers.SerializerMethodField()
    
    class Meta:
        model = HDThue
        fields = [
            'id',
            'khach_thue',
            'start_date',
            'end_date',
            'dk_gia_han',
            'gia_thue_per_month',
            'gia_thue_per_month_nt',
            'ky_tt',
            'tien_dat_coc',
            'tien_dat_coc_nt',
            'note',
            'ngoai_te',
            'ty_gia',
            'ngay_lay_ti_gia',
            'ngay_ki',
            'ngay_nhan',
            'ngay_tra',
            'type_contract',
            'services'
        ]
    
    def get_services(self, obj):
        return HD2DichVusResponseSerializer(obj.list_service, many=True).data


class HDMoiGioiResponseSerializer(serializers.ModelSerializer):
    tenant = TenantResponseSerializer()
    
    class Meta:
        model = HDMoiGioi
        fields = [
            'id',
            'tenant',
            'tien_moi_gioi',
            'note',
            'type_contract'
        ]


class HDDichVuResponseSerializer(serializers.ModelSerializer):
    tenant = TenantResponseSerializer()
    
    class Meta:
        model = HDDichVu
        fields = [
            'id',
            'tenant',
            'tien_thuc_linh',
            'tien_dich_vu',
            'thoi_gian_thanh_toan',
            'note',
            'type_contract'
        ]


class HDGroupResponseSerializer(serializers.ModelSerializer):
    can_ho = CanHoResponseSerializer()
    hd_thues = SubHDThueResponseSerializer(many=True)
    hd_moi_giois = HDMoiGioiResponseSerializer(many=True)
    hd_dich_vus = HDDichVuResponseSerializer(many=True)
    
    class Meta:
        model = HDGroups
        fields = [
            'id',
            'name',
            'can_ho',
            'hd_thues',
            'hd_moi_giois',
            'hd_dich_vus',
            'created_at',
        ]


class SubHDGroupResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDGroups
        fields = [
            'id',
            'name',
            'can_ho',
            'created_at',
        ]
