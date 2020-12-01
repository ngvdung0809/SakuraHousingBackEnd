from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from apps.contract.models import HD2DichVus
from apps.utils.constants import PaymentStatus

CHOICE_STATUS = (
    (PaymentStatus.PAID.value, "Paid"),
    (PaymentStatus.UNPAID.value, "Unpaid"),
    (PaymentStatus.ERROR.value, "Error"),
)


class PaymentTransactions(models.Model):
    hop_dong_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='hop_dong_type')
    hop_dong_id = models.PositiveIntegerField()
    nguoi_gui_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='nguoi_gui_type')
    nguoi_gui_id = models.PositiveIntegerField()
    nguoi_nhan_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='nguoi_nhan_type')
    nguoi_nhan_id = models.PositiveIntegerField()
    hop_dong = GenericForeignKey('hop_dong_type', 'hop_dong_id')
    dot_thanh_toan = models.CharField(max_length=512)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.IntegerField(choices=CHOICE_STATUS, default=PaymentStatus.UNPAID.value)  # choice
    ngay_thanh_toan_du_kien = models.DateField()
    ngay_thanh_toan_tt = models.DateField(null=True, blank=True)
    so_tien = models.IntegerField()
    nguoi_gui = GenericForeignKey('nguoi_gui_type', 'nguoi_gui_id')
    nguoi_nhan = GenericForeignKey('nguoi_nhan_type', 'nguoi_nhan_id')

    class Meta:
        db_table = 'payment_transaction'

    def __str__(self):
        return '{}'.format(self.id)


class ServiceTransactions(models.Model):
    hd_2_dichvu = models.ForeignKey(HD2DichVus, on_delete=models.CASCADE)
    dot_thanh_toan = models.CharField(max_length=512)
    so_tien = models.IntegerField(null=True, blank=True)
    ngay_thanh_toan_du_kien = models.DateField()
    ngay_thanh_toan_tt = models.DateField(null=True, blank=True)
    status = models.IntegerField(choices=CHOICE_STATUS, default=PaymentStatus.UNPAID.value)  # choice
    note = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        db_table = 'service_transaction'

    def __str__(self):
        return '{}-{}'.format(self.id, self.hd_2_dichvu)
