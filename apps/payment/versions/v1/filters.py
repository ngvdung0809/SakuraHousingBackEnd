from django_filters import rest_framework as filters

from apps.payment.models import PaymentTransactions, ServiceTransactions


class PaymentTransactionFilter(filters.FilterSet):
    can_ho = filters.NumberFilter(method='payment_filter')

    class Meta:
        model = PaymentTransactions
        fields = ['can_ho']

    def payment_filter(self, queryset, name, value):
        return queryset.filter(**{'hop_dong__hd_group__can_ho__id': value})


class ServiceTransactionFilter(filters.FilterSet):
    can_ho = filters.NumberFilter(field_name='can_ho', method='service_filter')

    class Meta:
        model = ServiceTransactions
        fields = ['can_ho']

    def service_filter(self, queryset, name, value):
        return queryset.filter(**{'hd_2_dichvu__hd_thue__hd_group__can_ho__id': value})
