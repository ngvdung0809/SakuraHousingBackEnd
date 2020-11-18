from django.db import transaction
from rest_framework import serializers

from apps.authentication.models import Accounts, Tenants
from apps.common.versions.v1.serializers.response_serializer import DichVuResponseSerializer
from apps.contract.models import HDGroups, HDMoiGioi, HDDichVu, HDThue, HD2DichVus, DichVus
from apps.contract.utils.create_payment import generate_payment_hd, generate_service
from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException


class HD2DichVusRequestSerializer(serializers.ModelSerializer):
    dich_vu = serializers.IntegerField()
    dinh_muc = serializers.IntegerField(required=False)
    note = serializers.CharField(max_length=255, required=False)
    
    class Meta:
        model = HD2DichVus
        fields = [
            'dich_vu',
            'ky_tt',
            'dinh_muc',
            'note',
        ]


class HDThueRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDThue
        fields = [
            'khach_thue',
            'nhan_vien',
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
        ]
    
    # def create(self, validated_data):
    #     hd_moi_gioi = HDMoiGioi.objects.create(**self.validated_data)
    #     return hd_moi_gioi
    
    def update(self, instance, validated_data):
        for i in validated_data.keys():
            setattr(instance, i, validated_data[i])
        instance.save()
        return instance


class HDMoiGioiRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDMoiGioi
        fields = [
            'tenant',
            'nhan_vien',
            'tien_moi_gioi',
            'note'
        ]
    
    # def create(self, validated_data):
    #     hd_moi_gioi = HDMoiGioi.objects.create(**self.validated_data)
    #     return hd_moi_gioi
    
    def update(self, instance, validated_data):
        for i in validated_data.keys():
            setattr(instance, i, validated_data[i])
        instance.save()
        return instance


class HDDichVuRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDDichVu
        fields = [
            'tenant',
            'nhan_vien',
            'tien_thuc_linh',
            'tien_dich_vu',
            'thoi_gian_thanh_toan',
            'note',
        ]
    
    # def create(self, validated_data):
    #     hd_dich_vu = HDDichVu.objects.create(**self.validated_data)
    #     return hd_dich_vu
    
    def update(self, instance, validated_data):
        for i in validated_data.keys():
            setattr(instance, i, validated_data[i])
        instance.save()
        return instance


class SubHDThueRequestSerializer(serializers.ModelSerializer):
    dich_vu = HD2DichVusRequestSerializer(many=True)
    
    class Meta:
        model = HDThue
        fields = [
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
            'dich_vu'
        ]


class SubHDMoiGioiRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDMoiGioi
        fields = [
            'tien_moi_gioi',
            'note'
        ]


class SubHDDichVuRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDDichVu
        fields = [
            'tien_thuc_linh',
            'tien_dich_vu',
            'thoi_gian_thanh_toan',
            'note',
        ]


class HDGroupRequestSerializer(serializers.ModelSerializer):
    nhan_vien = serializers.IntegerField()
    tenant = serializers.IntegerField()
    hd_thue = SubHDThueRequestSerializer()
    hd_moi_gioi = SubHDMoiGioiRequestSerializer()
    hd_dich_vu = SubHDDichVuRequestSerializer()
    
    def validate(self, attrs):
        try:
            nhan_vien = Accounts.objects.get(pk=attrs['nhan_vien'])
            tenant = Tenants.objects.get(pk=attrs['tenant'])
            
            return attrs
        except Accounts.DoesNotExist:
            raise CustomException(ErrorCode.not_found_record)
        except Tenants.DoesNotExist:
            raise CustomException(ErrorCode.not_found_record)
    
    class Meta:
        model = HDGroups
        fields = [
            'id',
            'name',
            'can_ho',
            'nhan_vien',
            'tenant',
            'hd_thue',
            'hd_moi_gioi',
            'hd_dich_vu',
        ]
    
    def create_hd2_dv(self, dich_vus, hd_thue):
        list_obj = [HD2DichVus(
            hd_thue=hd_thue,
            dich_vu_id=i['dich_vu'],
            ky_tt=i['ky_tt'],
            dinh_muc=i.get('dinh_muc', None),
            note=i.get('note', None)
        ) for i in dich_vus]
        list_instance = HD2DichVus.objects.bulk_create(list_obj)
        return list_instance
    
    @transaction.atomic
    def create(self, validated_data):
        hd_group = HDGroups.objects.create(**{
            'name': self.validated_data['name'],
            'can_ho': self.validated_data['can_ho'],
            'created_by': self.context['request'].user,
            'updated_by': self.context['request'].user,
        })
        
        self.validated_data['hd_thue']['hd_group'] = hd_group
        self.validated_data['hd_thue']['nhan_vien_id'] = self.validated_data['nhan_vien']
        
        self.validated_data['hd_moi_gioi']['hd_group'] = hd_group
        self.validated_data['hd_moi_gioi']['nhan_vien_id'] = self.validated_data['nhan_vien']
        self.validated_data['hd_moi_gioi']['tenant_id'] = self.validated_data['tenant']
        
        self.validated_data['hd_dich_vu']['hd_group'] = hd_group
        self.validated_data['hd_dich_vu']['nhan_vien_id'] = self.validated_data['nhan_vien']
        self.validated_data['hd_dich_vu']['tenant_id'] = self.validated_data['tenant']
        
        list_dv = self.validated_data['hd_thue']['dich_vu']
        self.validated_data['hd_thue'].pop('dich_vu')
        
        hd_thue = HDThue.objects.create(**self.validated_data['hd_thue'])
        hd_moi_gioi = HDMoiGioi.objects.create(**self.validated_data['hd_moi_gioi'])
        HDDichVu.objects.create(**self.validated_data['hd_dich_vu'])
        
        services = self.create_hd2_dv(list_dv, hd_thue)
        
        generate_payment_hd(hd_thue, hd_moi_gioi, self.validated_data['can_ho'].chu_nha)
        generate_service(services, self.validated_data['hd_thue']['start_date'],
                         self.validated_data['hd_thue']['end_date'])
        
        return hd_group
    
    # def update(self, instance, validated_data):
    #     validated_data['updated_by'] = self.context['request'].user
    #     for i in validated_data.keys():
    #         setattr(instance, i, validated_data[i])
    #     instance.save()
    #     return instance
