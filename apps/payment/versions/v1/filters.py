from django.contrib.contenttypes.models import ContentType
from django.db.models.query_utils import Q
from django_filters import rest_framework as filters

from apps.contract.models import HDThue, HDMoiGioi
from apps.payment.models import PaymentTransactions, ServiceTransactions


class PaymentTransactionFilter(filters.FilterSet):
    can_ho = filters.NumberFilter(method='payment_filter')
    
    class Meta:
        model = PaymentTransactions
        fields = ['can_ho']
    
    def payment_filter(self, queryset, name, value):
        hd_thue = HDThue.objects.filter(hd_group__can_ho_id=value)
        hd_moigioi = HDMoiGioi.objects.filter(hd_group__can_ho_id=value)
        return queryset.filter(
            Q(hop_dong_id__in=hd_thue.values_list('pk', flat=True),
              hop_dong_type=ContentType.objects.get_for_model(HDThue).id) |
            Q(hop_dong_id__in=hd_moigioi.values_list('pk', flat=True),
              hop_dong_type=ContentType.objects.get_for_model(
                  HDMoiGioi).id)
        )


class ServiceTransactionFilter(filters.FilterSet):
    can_ho = filters.NumberFilter(field_name='can_ho', method='service_filter')
    dich_vu = filters.NumberFilter(method='dich_vu_filter')
    
    class Meta:
        model = ServiceTransactions
        fields = ['can_ho', 'dich_vu']
    
    def service_filter(self, queryset, name, value):
        return queryset.filter(**{'hd_2_dichvu__hd_thue__hd_group__can_ho_id': value})
    
    def dich_vu_filter(self, queryset, name, value):
        return queryset.filter(**{'hd_2_dichvu__dich_vu_id': value})
