from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Prefetch
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

    def validate_ky_tt(self, value):
        if value < 1:
            raise CustomException(ErrorCode.error_json_parser)
        return value

    class Meta:
        model = HD2DichVus
        fields = [
            'dich_vu',
            'ky_tt',
            'dinh_muc',
            'note',
        ]


class SubHDThueRequestSerializer(serializers.ModelSerializer):
    dich_vu = HD2DichVusRequestSerializer(many=True, required=False)

    def validate_ky_tt(self, value):
        if value < 1:
            raise CustomException(ErrorCode.error_json_parser)
        return value

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
        extra_kwargs = {"dich_vu": {"required": False, "allow_null": True}}


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
    hd_thue = SubHDThueRequestSerializer()
    hd_moi_gioi = SubHDMoiGioiRequestSerializer(required=False, allow_null=True)
    hd_dich_vu = SubHDDichVuRequestSerializer(required=False, allow_null=True)

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
        extra_kwargs = {
            "dich_vu": {"required": False, "allow_null": True},
            "hd_moi_gioi": {"required": False, "allow_null": True},
            "hd_dich_vu": {"required": False, "allow_null": True},
        }

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
        if 'hd_moi_gioi' in self.validated_data:
            self.validated_data['hd_moi_gioi']['hd_group'] = hd_group
            hd_moi_gioi = HDMoiGioi.objects.create(**self.validated_data['hd_moi_gioi'])
        if 'hd_dich_vu' in self.validated_data:
            self.validated_data['hd_dich_vu']['hd_group'] = hd_group
            HDDichVu.objects.create(**self.validated_data['hd_dich_vu'])

        list_dv = self.validated_data['hd_thue'].get('dich_vu', None)
        self.validated_data['hd_thue'].pop('dich_vu', None)

        hd_thue = HDThue.objects.create(**self.validated_data['hd_thue'])

        if list_dv:
            services = create_hd2_dv(list_dv, hd_thue)
            generate_service(services, self.validated_data['hd_thue']['start_date'],
                             self.validated_data['hd_thue']['end_date'])

        generate_payment_hd(
            hd_thue,
            hd_moi_gioi,
            self.validated_data['can_ho'].chu_nha,
            self.validated_data['nhan_vien'].tenant
        )

        return hd_group

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        # update hd groups
        for i in self.validated_data.keys():
            setattr(instance, i, self.validated_data[i])
        instance.save()

        # update hd thue
        if 'hd_thue' in validated_data:
            try:
                hd_instance = HDThue.objects.select_related(
                    'hd_group__nhan_vien__tenant',
                    'hd_group__can_ho__chu_nha'
                ).prefetch_related(
                    Prefetch(
                        'hd2dichvus_set',
                        queryset=HD2DichVus.objects.select_related('dich_vu').all(),
                        to_attr='list_service'
                    )
                ).get(hd_group_id=instance.id)
                self.update_instance(hd_instance, key='hd_thue')
            except HDThue.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)

        # update hd moi gioi
        if 'hd_moi_gioi' in validated_data:
            try:
                mg_instance = HDMoiGioi.objects.get(hd_group_id=instance.id)
                self.update_instance(mg_instance, key='hd_moi_gioi')
            except HDMoiGioi.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)

        # update hd dich vu
        if 'hd_dich_vu' in validated_data:
            try:
                dv_instance = HDDichVu.objects.get(hd_group_id=instance.id)
                self.update_instance(dv_instance, key='hd_dich_vu')
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
            hd_2_dv = None
            self.validated_data['hd_thue'].pop('dich_vu', None)
            if dich_vu or any(key in self.validated_data['hd_thue'] for key in ['start_date', 'end_date']):
                if not dich_vu:
                    hd_2_dv = instance.list_service
                self.update_dv(instance, dich_vu, hd_2_dv)

            if any(key in self.validated_data['hd_thue'] for key in
                   ['gia_thue_per_month', 'start_date', 'end_date', 'ky_tt']):
                PaymentTransactions.objects.filter(
                    hop_dong_id=instance.id,
                    hop_dong_type=ContentType.objects.get_for_model(instance).id
                ).delete()
                generate_payment_hd(
                    hd_thue=instance,
                    hd_moi_gioi=None,
                    chu_nha=instance.hd_group.can_ho.chu_nha,
                    tenant=instance.hd_group.nhan_vien.tenant
                )
        return instance

    def delete_dv(self, hd_thue):
        list_instance = HD2DichVus.objects.filter(hd_thue=hd_thue)

        ServiceTransactions.objects.filter(hd_2_dichvu__in=list_instance).delete()
        list_instance.delete()

    def update_dv(self, instance, dich_vu, hd_2_dv):
        if not hd_2_dv:
            self.delete_dv(instance)
            hd_2_dv = create_hd2_dv(dich_vu, instance)
        generate_service(hd_2_dv, instance.start_date, instance.end_date)
