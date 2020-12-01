from rest_framework import serializers

from apps.common.models import ToaNhas, ChuNhas, KhachThues, CanHos, Districts
from apps.contract.models import DichVus


class DistrictResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Districts
        fields = '__all__'


class ToaNhaResponseSerializer(serializers.ModelSerializer):
    district = DistrictResponseSerializer()
    
    class Meta:
        model = ToaNhas
        fields = ['id', 'name', 'address', 'phuong', 'district', 'city']


class ChuNhaResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChuNhas
        fields = ['id', 'name', 'cmt', 'cmt_NgayCap', 'cmt_NoiCap', 'cccd', 'cccd_NgayCap', 'cccd_NoiCap',
                  'passport_no', 'passport_NgayCap', 'passport_NgayHan', 'birthday',
                  'address', 'phone', 'phone2', 'email', 'email2', 'so_TK', 'chi_nhanh', 'ngan_hang', 'so_TK2',
                  'chi_nhanh2', 'ngan_hang2', 'note', ]


class KhachThueResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KhachThues
        fields = [
            'id',
            'name',
            'cmt',
            'cmt_NgayCap',
            'cmt_NoiCap',
            'cccd',
            'cccd_NgayCap',
            'cccd_NoiCap',
            'passport_no',
            'passport_NgayCap',
            'passport_NgayHan',
            'company_name',
            'company_phone',
            'company_fax',
            'company_address',
            'company_tax_code',
            'company_rep',
            'company_rep_role',
            'birthday',
            'address',
            'phone',
            'email',
            'assistant_name',
            'assistant_phone',
            'assistant_email',
            'note'
        ]


class CanHoResponseSerializer(serializers.ModelSerializer):
    chu_nha = ChuNhaResponseSerializer()
    toa_nha = ToaNhaResponseSerializer()
    
    class Meta:
        model = CanHos
        fields = [
            'id',
            'name',
            'chu_nha',
            'toa_nha',
            'address',
            'gcn',
            'gcn_NgayCap',
            'gcn_NoiCap',
            'description',
            'note'
        ]


class DichVuResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DichVus
        fields = [
            'id',
            'name',
            'don_vi',
            'code',
            'dinh_ky',
        ]
