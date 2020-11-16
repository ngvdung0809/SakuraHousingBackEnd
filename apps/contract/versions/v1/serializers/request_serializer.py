from django.db.models import Prefetch
from rest_framework import serializers

from apps.authentication.models import Accounts, Tenants
from apps.contract.models import HDGroups, HDMoiGioi, HDDichVu, HDThue
from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException


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

        HDThue.objects.create(**self.validated_data['hd_thue'])
        HDMoiGioi.objects.create(**self.validated_data['hd_moi_gioi'])
        HDDichVu.objects.create(**self.validated_data['hd_dich_vu'])

        return hd_group

    # def update(self, instance, validated_data):
    #     validated_data['updated_by'] = self.context['request'].user
    #     for i in validated_data.keys():
    #         setattr(instance, i, validated_data[i])
    #     instance.save()
    #     return instance
