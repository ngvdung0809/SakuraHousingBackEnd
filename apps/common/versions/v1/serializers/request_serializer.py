from rest_framework import serializers

from apps.common.models import ToaNhas, ChuNhas, CanHos, KhachThues
from apps.contract.models import DichVus


class ToaNhaRequestSerializer(serializers.ModelSerializer):
    address = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    phuong = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    city = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)

    class Meta:
        model = ToaNhas
        fields = ['name', 'address', 'phuong', 'district', 'city']

    def create(self, validated_data):
        toa_nha = ToaNhas.objects.create(**self.validated_data)
        return toa_nha

    def update(self, instance, validated_data):
        for i in validated_data.keys():
            setattr(instance, i, validated_data[i])
        instance.save()
        return instance


class ChuNhaRequestSerializer(serializers.ModelSerializer):
    cmt = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    cmt_NgayCap = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    cmt_NoiCap = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    cccd = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    cccd_NgayCap = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    cccd_NoiCap = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    passport_no = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    passport_NgayCap = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    passport_NgayHan = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    birthday = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone2 = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    email2 = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    so_TK2 = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    chi_nhanh2 = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    ngan_hang2 = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    note = serializers.CharField(allow_null=True, allow_blank=True, max_length=512)

    class Meta:
        model = ChuNhas
        fields = ['name', 'cmt', 'cmt_NgayCap', 'cmt_NoiCap', 'cccd', 'cccd_NgayCap', 'cccd_NoiCap',
                  'passport_no', 'passport_NgayCap', 'passport_NgayHan', 'birthday',
                  'address', 'phone', 'phone2', 'email', 'email2', 'so_TK', 'chi_nhanh', 'ngan_hang', 'so_TK2',
                  'chi_nhanh2', 'ngan_hang2', 'note', ]

    def create(self, validated_data):
        chu_nha = ChuNhas.objects.create(**self.validated_data)
        return chu_nha

    def update(self, instance, validated_data):
        for i in validated_data.keys():
            if validated_data[i] == "":
                setattr(instance, i, None)
            else:
                setattr(instance, i, validated_data[i])
        instance.save()
        return instance


class CanHoRequestSerializer(serializers.ModelSerializer):
    description = serializers.CharField(allow_null=True, allow_blank=True, max_length=512)
    note = serializers.CharField(allow_null=True, allow_blank=True, max_length=512)

    class Meta:
        model = CanHos
        fields = [
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

    def create(self, validated_data):
        can_ho = CanHos.objects.create(**self.validated_data)
        return can_ho

    def update(self, instance, validated_data):
        for i in validated_data.keys():
            setattr(instance, i, validated_data[i])
        instance.save()
        return instance


class KhachThueRequestSerializer(serializers.ModelSerializer):
    cmt = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    cmt_NgayCap = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    cmt_NoiCap = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    cccd = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    cccd_NgayCap = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    cccd_NoiCap = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    passport_no = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    passport_NgayCap = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    passport_NgayHan = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    company_name = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    company_phone = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    company_fax = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    company_address = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    company_tax_code = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    company_rep = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    company_rep_role = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    birthday = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    assistant_name = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    assistant_phone = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    assistant_email = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    note = serializers.CharField(allow_null=True, allow_blank=True, max_length=512)

    class Meta:
        model = KhachThues
        fields = [
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

    def create(self, validated_data):
        khach_thue = KhachThues.objects.create(**self.validated_data)
        return khach_thue

    def update(self, instance, validated_data):
        for i in validated_data.keys():
            if validated_data[i] == "":
                setattr(instance, i, None)
            else:
                setattr(instance, i, validated_data[i])
        instance.save()
        return instance


class DichVuRequestSerializer(serializers.ModelSerializer):
    don_vi = serializers.CharField(max_length=10, allow_null=True, allow_blank=True)
    code = serializers.CharField(max_length=10, allow_null=True, allow_blank=True)
    dinh_ky = serializers.BooleanField(default=True)

    class Meta:
        model = DichVus
        fields = [
            'name',
            'don_vi',
            'code',
            'dinh_ky',
        ]

    def create(self, validated_data):
        dich_vu = DichVus.objects.create(**self.validated_data)
        return dich_vu

    def update(self, instance, validated_data):
        for i in validated_data.keys():
            setattr(instance, i, validated_data[i])
        instance.save()
        return instance
