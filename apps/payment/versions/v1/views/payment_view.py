from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import apps.utils.response_interface as rsp
from apps.common.models import ToaNhas, ChuNhas, KhachThues, CanHos
from apps.common.versions.v1.serializers.request_serializer import ToaNhaRequestSerializer, ChuNhaRequestSerializer, \
    KhachThueRequestSerializer, CanHoRequestSerializer, DichVuRequestSerializer
from apps.common.versions.v1.serializers.response_serializer import ToaNhaResponseSerializer, \
    ChuNhaResponseSerializer, KhachThueResponseSerializer, CanHoResponseSerializer, DichVuResponseSerializer
from apps.contract.models import DichVus
from apps.payment.models import PaymentTransactions, ServiceTransactions
from apps.payment.versions.v1.serializers.response_serializer import PaymentTransactionResponseSerializer
from apps.utils.constants import PaymentStatus
from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException
from apps.utils.permission import IsAdminRole
from apps.utils.views_helper import GenericViewSet


class PaymentView:
    start_date = openapi.Parameter('start_date', openapi.IN_QUERY,
                                   description="start_date",
                                   type=openapi.TYPE_STRING)
    end_date = openapi.Parameter('end_date', openapi.IN_QUERY,
                                 description="end_date",
                                 type=openapi.TYPE_STRING)

    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class PaymentViewSet(GenericViewSet):
        serializer_class = ToaNhaRequestSerializer
        queryset = ToaNhas.objects.all()
        action_serializers = {
            'list_payment': PaymentTransactionResponseSerializer,
            'list_toa_nha_response': ToaNhaResponseSerializer,
            'partial_update_response': ToaNhaResponseSerializer,
            'detail_toa_nha_response': ToaNhaResponseSerializer
        }
        permission_classes = [IsAdminRole]

        def list(self, request, custom_queryset=None, custom_query_params=None, *args, **kwargs):
            pass

        def retrieve(self, request, custom_object=None, *args, **kwargs):
            pass

        def destroy(self, request, *args, **kwargs):
            pass

        def partial_update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
            pass

        def create(self, request, *args, **kwargs):
            pass

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-payment')
        def list_payment(self, request, *args, **kwargs):
            start_date = ''
            end_date = ''
            query = PaymentTransactions.objects.prefetch_related(
                'hop_dong', 'hop_dong__hd_group__can_ho'
            ).all()
            if start_date:
                query = query.filter(ngay_thanh_toan_du_kien__gte=start_date)
            if end_date:
                query = query.filter(ngay_thanh_toan_du_kien__lte=end_date)

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-service-payment')
        def list_service_payment(self, request, *args, **kwargs):
            start_date = ''
            end_date = ''
            query = ServiceTransactions.objects.select_related(
                'hd_2_dichvu__dich_vu', 'hd_2_dichvu__hd_thue__hd_group__can_ho',
            ).all()
            if start_date:
                query = query.filter(ngay_thanh_toan_du_kien__gte=start_date)
            if end_date:
                query = query.filter(ngay_thanh_toan_du_kien__lte=end_date)

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-unpaid-payment')
        def list_unpaid_payment(self, request, *args, **kwargs):
            query = PaymentTransactions.objects.prefetch_related(
                'hop_dong', 'hop_dong__hd_group__can_ho'
            ).filter(status=PaymentStatus.UNPAID.value, end_date__lt=timezone.now()).all()

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'],
                url_path='list-unpaid-service-payment')
        def list_unpaid_service_payment(self, request, *args, **kwargs):
            query = ServiceTransactions.objects.select_related(
                'hd_2_dichvu__dich_vu', 'hd_2_dichvu__hd_thue__hd_group__can_ho',
            ).filter(status=PaymentStatus.UNPAID.value, end_date__lt=timezone.now()).all()

        @action(detail=False, permission_classes=[IsAdminRole], methods=['post'], url_path='service-payment')
        def service_payment(self, request, *args, **kwargs):
            pass

        @action(detail=False, permission_classes=[IsAdminRole], methods=['post'], url_path='payment')
        def payment(self, request, *args, **kwargs):
            pass
