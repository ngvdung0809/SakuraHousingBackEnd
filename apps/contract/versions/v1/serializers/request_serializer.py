from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import serializers

from apps.authentication.models import Accounts, Tenants
from apps.contract.models import HDGroups, HDMoiGioi, HDDichVu, HDThue, HD2DichVus
from apps.contract.utils.create_payment import generate_payment_hd, generate_service, create_hd2_dv
from apps.payment.models import ServiceTransactions, PaymentTransactions
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
    hd_thue = SubHDThueRequestSerializer()
    hd_moi_gioi = SubHDMoiGioiRequestSerializer()
    hd_dich_vu = SubHDDichVuRequestSerializer()

    def validate(self, attrs):
        try:
            nhan_vien = Accounts.objects.get(pk=attrs['nhan_vien'])
            attrs['nhan_vien'] = nhan_vien
            return attrs
        except Accounts.DoesNotExist:
            raise CustomException(ErrorCode.not_found_record)

    class Meta:
        model = HDGroups
        fields = [
            'id',
            'name',
            'can_ho',
            'nhan_vien',
            'hd_thue',
            'hd_moi_gioi',
            'hd_dich_vu',
        ]

    @transaction.atomic
    def create(self, validated_data):
        hd_group = HDGroups.objects.create(**{
            'name': self.validated_data['name'],
            'can_ho': self.validated_data['can_ho'],
            'nhan_vien': self.validated_data['nhan_vien'],
            'created_by': self.context['request'].user,
            'updated_by': self.context['request'].user,
        })

        hd_moi_gioi = None

        self.validated_data['hd_thue']['hd_group'] = hd_group
        if self.validated_data['hd_moi_gioi']:
            self.validated_data['hd_moi_gioi']['hd_group'] = hd_group
            hd_moi_gioi = HDMoiGioi.objects.create(**self.validated_data['hd_moi_gioi'])
        if self.validated_data['hd_dich_vu']:
            self.validated_data['hd_dich_vu']['hd_group'] = hd_group
            HDDichVu.objects.create(**self.validated_data['hd_dich_vu'])

        list_dv = self.validated_data['hd_thue']['dich_vu']
        self.validated_data['hd_thue'].pop('dich_vu')

        hd_thue = HDThue.objects.create(**self.validated_data['hd_thue'])

        services = create_hd2_dv(list_dv, hd_thue)

        generate_payment_hd(hd_thue, hd_moi_gioi, self.validated_data['can_ho'].chu_nha)
        generate_service(services, self.validated_data['hd_thue']['start_date'],
                         self.validated_data['hd_thue']['end_date'])

        return hd_group

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        # update hd groups
        for i in self.validated_data.keys():
            setattr(instance, i, self.validated_data[i])
        instance.save()

        # update hd thue
        if validated_data['hd_thue']:
            try:
                instance = HDThue.objects.get(hd_group_id=instance.id)
                self.update_instance(instance, key='hd_thue')
            except HDThue.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)

        # update hd moi gioi
        if validated_data['hd_moi_gioi']:
            try:
                instance = HDMoiGioi.objects.get(hd_group_id=instance.id)
                self.update_instance(instance, key='hd_moi_gioi')
            except HDMoiGioi.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)

        # update hd dich vu
        if validated_data['hd_dich_vu']:
            try:
                instance = HDDichVu.objects.get(hd_group_id=instance.id)
                self.update_instance(instance, key='hd_dich_vu')
            except HDDichVu.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
        return instance

    @transaction.atomic
    def update_instance(self, instance, key):
        for i in self.validated_data[key].keys():
            setattr(instance, i, self.validated_data[key][i])
        instance.save()

        if key == 'hd_thue':
            dich_vu = self.validated_data['hd_thue'].get('dich_vu', None)
            self.validated_data['hd_thue'].pop('dich_vu', None)
            if dich_vu or any(key in self.validated_data['hd_thue'] for key in ['start_date', 'end_date']):
                self.update_dv(instance, dich_vu)

            if any(key in self.validated_data['hd_thue'] for key in
                   ['gia_thue_per_month', 'start_date', 'end_date', 'ky_tt']):
                PaymentTransactions.objects.filter(
                    hop_dong_id=instance.id,
                    hop_dong_type=ContentType.objects.get_for_model(instance).id
                ).delete()
                generate_payment_hd(hd_thue=instance, hd_moi_gioi=None, chu_nha=instance.hd_group.can_ho.chu_nha)
        return instance

    def delete_dv(self, hd_thue):
        list_instance = HD2DichVus.objects.filter(hd_thue=hd_thue)

        ServiceTransactions.objects.filter(hd_2_dichvu__in=list_instance).delete()
        list_instance.delete()

    def update_dv(self, instance, dich_vu):
        self.delete_dv(instance)
        services = create_hd2_dv(dich_vu, instance)
        generate_service(services, instance.start_date, instance.end_date)
