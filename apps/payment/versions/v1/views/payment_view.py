from datetime import datetime

from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as filters

import apps.utils.response_interface as rsp
from SakuraHousing import settings
from apps.common.models import ToaNhas, ChuNhas, KhachThues, CanHos
from apps.common.versions.v1.serializers.request_serializer import ToaNhaRequestSerializer, ChuNhaRequestSerializer, \
    KhachThueRequestSerializer, CanHoRequestSerializer, DichVuRequestSerializer
from apps.common.versions.v1.serializers.response_serializer import ToaNhaResponseSerializer, \
    ChuNhaResponseSerializer, KhachThueResponseSerializer, CanHoResponseSerializer, DichVuResponseSerializer
from apps.contract.models import DichVus
from apps.payment.models import PaymentTransactions, ServiceTransactions
from apps.payment.versions.v1.filters import PaymentTransactionFilter
from apps.payment.versions.v1.serializers.request_serializer import PaymentHDRequestSerializer, \
    PaymentServiceRequestSerializer, PaymentEmailRequestSerializer
from apps.payment.versions.v1.serializers.response_serializer import PaymentTransactionResponseSerializer, \
    ServiceTransactionResponseSerializer
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
    # @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list_payment', decorator=swagger_auto_schema(
        manual_parameters=[start_date, end_date]
    ))
    @method_decorator(name='list_service_payment', decorator=swagger_auto_schema(
        manual_parameters=[start_date, end_date]
    ))
    class PaymentViewSet(GenericViewSet):
        serializer_class = PaymentTransactionResponseSerializer
        queryset = PaymentTransactions.objects.all()
        action_serializers = {
            'list_payment': PaymentTransactionResponseSerializer,
            'payment_request': PaymentHDRequestSerializer,
            'service_payment_request': PaymentServiceRequestSerializer,
            'send_mail_payment_request': PaymentEmailRequestSerializer
        }
        permission_classes = [IsAdminRole]
        filterset_class = PaymentTransactionFilter

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
            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)
            query = PaymentTransactions.objects.prefetch_related(
                'hop_dong', 'hop_dong__hd_group__can_ho', 'nguoi_gui', 'nguoi_nhan'
            ).order_by('ngay_thanh_toan_du_kien').all()
            if start_date:
                start = datetime.strptime(start_date, settings.DATE_FORMATS[1])
                query = query.filter(ngay_thanh_toan_du_kien__gte=start)
            if end_date:
                end = datetime.strptime(end_date, settings.DATE_FORMATS[1])
                query = query.filter(ngay_thanh_toan_du_kien__lte=end)
            results = PaymentTransactionResponseSerializer(query, many=True).data
            return super().custom_response(results)

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-service-payment')
        def list_service_payment(self, request, *args, **kwargs):
            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)
            query = ServiceTransactions.objects.select_related(
                'hd_2_dichvu__dich_vu', 'hd_2_dichvu__hd_thue__hd_group__can_ho',
            ).order_by('ngay_thanh_toan_du_kien').all()
            if start_date:
                start = datetime.strptime(start_date, settings.DATE_FORMATS[1])
                query = query.filter(ngay_thanh_toan_du_kien__gte=start)
            if end_date:
                end = datetime.strptime(end_date, settings.DATE_FORMATS[1])
                query = query.filter(ngay_thanh_toan_du_kien__lte=end)
            results = ServiceTransactionResponseSerializer(query, many=True).data
            res = self.filter_service(results)
            return super().custom_response(res)

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-unpaid-payment')
        def list_unpaid_payment(self, request, *args, **kwargs):
            query = PaymentTransactions.objects.prefetch_related(
                'hop_dong', 'hop_dong__hd_group__can_ho', 'nguoi_gui', 'nguoi_nhan'
            ).order_by('ngay_thanh_toan_du_kien').filter(status=PaymentStatus.UNPAID.value,
                                                         end_date__lt=timezone.now()).all()
            results = PaymentTransactionResponseSerializer(query, many=True).data
            return super().custom_response(results)

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'],
                url_path='list-unpaid-service-payment')
        def list_unpaid_service_payment(self, request, *args, **kwargs):
            query = ServiceTransactions.objects.select_related(
                'hd_2_dichvu__dich_vu', 'hd_2_dichvu__hd_thue__hd_group__can_ho',
            ).order_by('ngay_thanh_toan_du_kien').filter(status=PaymentStatus.UNPAID.value,
                                                         ngay_thanh_toan_du_kien__lt=timezone.now()).all()
            results = ServiceTransactionResponseSerializer(query, many=True).data
            res = self.filter_service(results)
            return super().custom_response(res)

        @action(detail=False, permission_classes=[IsAdminRole], methods=['post'], url_path='service-payment')
        def service_payment(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            service_payment = serializer.save()

            general_response = rsp.Response(
                ServiceTransactionResponseSerializer(service_payment).data).generate_response()
            response = Response(general_response, status=status.HTTP_201_CREATED)
            return response

        @action(detail=False, permission_classes=[IsAdminRole], methods=['post'], url_path='payment')
        def payment(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            instance = serializer.save()

            general_response = rsp.Response(PaymentTransactionResponseSerializer(instance).data).generate_response()
            response = Response(general_response, status=status.HTTP_201_CREATED)
            return response

        @action(detail=False, permission_classes=[IsAdminRole], methods=['post'], url_path='send-mail-payment')
        def send_mail_payment(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return super().custom_response({})

        def filter_service(self, data):
            results = {}
            for i in data:
                if i['can_ho'] in results:
                    results[i['can_ho']].append(i)
                else:
                    results[i['can_ho']] = [i]
            return results
