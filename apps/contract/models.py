from django.db import models

# Create your models here.
from apps.authentication.models import Accounts, Tenants
from apps.common.models import CanHos, KhachThues


class HDGroups(models.Model):
    name = models.CharField(max_length=255)
    can_ho = models.ForeignKey(CanHos, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='hd_group_created_by')
    updated_by = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='hd_group_updated_by')
    
    class Meta:
        db_table = 'hd_group'
    
    def __str__(self):
        return '{}-{}-{}'.format(self.id, self.name, self.can_ho)


class ContractType(models.Model):
    name = models.CharField(max_length=255)
    can_ho = models.ForeignKey(CanHos, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    short_name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'contract_type'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.short_name)


class HDThue(models.Model):
    hd_group = models.ForeignKey(HDGroups, on_delete=models.CASCADE)
    khach_thue = models.ForeignKey(KhachThues, on_delete=models.CASCADE)
    nhan_vien = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    dk_gia_han = models.CharField(max_length=512)
    gia_thue_per_month = models.IntegerField(null=True, blank=True)
    gia_thue_per_month_nt = models.IntegerField(null=True, blank=True)
    ky_tt = models.IntegerField()
    tien_dat_coc = models.IntegerField()
    tien_dat_coc_nt = models.IntegerField()
    note = models.CharField(max_length=512, null=True, blank=True)
    ngoai_te = models.CharField(max_length=10)
    ty_gia = models.FloatField(null=True, blank=True)
    ngay_lay_ti_gia = models.DateField(null=True, blank=True)
    ngay_ki = models.DateField()
    ngay_nhan = models.DateField()
    ngay_tra = models.DateField()
    type_contract = models.ForeignKey(ContractType, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'hd_thue'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.hd_group)


class HDMoiGioi(models.Model):
    hd_group = models.ForeignKey(HDGroups, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    nhan_vien = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    tien_com = models.IntegerField()
    chi_phi = models.IntegerField()
    tien_chenh = models.IntegerField()
    tien_tra_ky = models.IntegerField()
    ky_tt = models.IntegerField()
    note = models.CharField(max_length=512, null=True, blank=True)
    type_contract = models.ForeignKey(ContractType, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'hd_moi_gioi'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.hd_group)


class HDDichVu(models.Model):
    hd_group = models.ForeignKey(HDGroups, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    nhan_vien = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    tien_thuc_linh = models.IntegerField()
    tien_dich_vu = models.IntegerField()
    thoi_gian_thanh_toan = models.CharField(max_length=255)
    note = models.CharField(max_length=512, null=True, blank=True)
    type_contract = models.ForeignKey(ContractType, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'hd_dich_vu'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.hd_group)


class DichVus(models.Model):
    name = models.CharField(max_length=255)
    don_vi = models.CharField(max_length=10, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    dinh_ky = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'dich_vu'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.name)


class HD2DichVus(models.Model):
    hd_thue = models.ForeignKey(HDThue, on_delete=models.CASCADE)
    dich_vu = models.ForeignKey(DichVus, on_delete=models.CASCADE)
    don_gia = models.IntegerField()
    ky_tt = models.IntegerField()
    dinh_muc = models.IntegerField()
    note = models.CharField(max_length=512, null=True, blank=True)
    payment = models.JSONField()
    
    class Meta:
        db_table = 'hd_2_dich_vu'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.hd_thue)
