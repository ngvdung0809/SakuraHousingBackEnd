from django.db import models

# Create your models here.
from apps.authentication.models import Accounts


class Districts(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'districts'

    def __str__(self):
        return '{}-{}'.format(self.id, self.name)


class ToaNhas(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    phuong = models.CharField(max_length=255, null=True, blank=True)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    city = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'toa_nhas'

    def __str__(self):
        return '{}-{}'.format(self.id, self.name)


class ChuNhas(models.Model):
    name = models.CharField(max_length=255)
    cmt = models.CharField(max_length=255, null=True, blank=True)
    cmt_NgayCap = models.DateField(null=True, blank=True)
    cmt_NoiCap = models.CharField(max_length=255, null=True, blank=True)
    cccd = models.CharField(max_length=255, null=True, blank=True)
    cccd_NgayCap = models.DateField(null=True, blank=True)
    cccd_NoiCap = models.CharField(max_length=255, null=True, blank=True)
    passport_no = models.CharField(max_length=255, null=True, blank=True)
    passport_NgayCap = models.DateField(null=True, blank=True)
    passport_NgayHan = models.DateField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    phone2 = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255)
    email2 = models.CharField(max_length=255, null=True, blank=True)
    so_TK = models.CharField(max_length=255)
    chi_nhanh = models.CharField(max_length=255)
    ngan_hang = models.CharField(max_length=255)
    so_TK2 = models.CharField(max_length=255, null=True, blank=True)
    chi_nhanh2 = models.CharField(max_length=255, null=True, blank=True)
    ngan_hang2 = models.CharField(max_length=255, null=True, blank=True)
    note = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chu_nhas'

    def __str__(self):
        return '{}-{}-{}'.format(self.id, self.name, self.cmt)


class KhachThues(models.Model):
    name = models.CharField(max_length=255)
    cmt = models.CharField(max_length=255, null=True, blank=True)
    cmt_NgayCap = models.DateField(null=True, blank=True)
    cmt_NoiCap = models.CharField(max_length=255, null=True, blank=True)
    cccd = models.CharField(max_length=255, null=True, blank=True)
    cccd_NgayCap = models.DateField(null=True, blank=True)
    cccd_NoiCap = models.CharField(max_length=255, null=True, blank=True)
    passport_no = models.CharField(max_length=255, null=True, blank=True)
    passport_NgayCap = models.DateField(null=True, blank=True)
    passport_NgayHan = models.DateField(null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_phone = models.CharField(max_length=255, null=True, blank=True)
    company_fax = models.CharField(max_length=255, null=True, blank=True)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    company_tax_code = models.CharField(max_length=255, null=True, blank=True)
    company_rep = models.CharField(max_length=255, null=True, blank=True)
    company_rep_role = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    assistant_name = models.CharField(max_length=255, null=True, blank=True)
    assistant_phone = models.CharField(max_length=255, null=True, blank=True)
    assistant_email = models.CharField(max_length=255, null=True, blank=True)
    note = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'khach_thues'

    def __str__(self):
        return '{}-{}-{}'.format(self.id, self.name, self.cmt)


class CanHos(models.Model):
    name = models.CharField(max_length=255)
    chu_nha = models.ForeignKey(ChuNhas, on_delete=models.CASCADE)
    toa_nha = models.ForeignKey(ToaNhas, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255)
    gcn = models.CharField(max_length=255)
    gcn_NgayCap = models.DateField(max_length=255)
    gcn_NoiCap = models.CharField(max_length=255)
    description = models.CharField(max_length=512, null=True, blank=True)
    note = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'can_hos'

    def __str__(self):
        return '{}-{}'.format(self.id, self.name)
