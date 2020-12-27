import datetime

from django.contrib.contenttypes.models import ContentType
from django.db.models.expressions import F, ExpressionWrapper
from django.db.models.fields import DateField, DurationField
from django.db.models.functions.comparison import Cast
from django.db.models.query import Prefetch
from django.db.models.query_utils import Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import apps.utils.response_interface as rsp
from apps.contract.models import HDGroups, HDThue, HDMoiGioi, HDDichVu, HD2DichVus
from apps.contract.versions.v1.serializers.request_serializer import HDGroupRequestSerializer
from apps.contract.versions.v1.serializers.response_serializer import HDGroupResponseSerializer, \
    HDThueResponseSerializer, SubHDGroupResponseSerializer, \
    HDThueExpiredResponseSerializer
from apps.payment.models import ServiceTransactions, PaymentTransactions
from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException
from apps.utils.multi_delete import MultiDeleteRequestSerializer
from apps.utils.permission import IsAdminRole
from apps.utils.views_helper import GenericViewSet


class HDGroupView:
    search_field = openapi.Parameter(
        'search',
        openapi.IN_QUERY,
        description="Tim kiem theo ten bo hop dong",
        type=openapi.TYPE_STRING
    )

    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    # @method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list_hd_group', decorator=swagger_auto_schema(
        manual_parameters=[search_field]
    ))
    class HDGroupViewSet(GenericViewSet):
        serializer_class = HDGroupRequestSerializer
        queryset = HDGroups.objects.all()
        permission_classes = [IsAdminRole]
        action_serializers = {
            'create_request': HDGroupRequestSerializer,
            'list_hd_group_response': HDGroupResponseSerializer,
            'partial_update_response': SubHDGroupResponseSerializer,
            'partial_update_request': HDGroupRequestSerializer,
            'detail_hd_group_response': HDGroupResponseSerializer,
            'delete_multi_request': MultiDeleteRequestSerializer
        }

        def common_query(self):
            query = HDGroups.objects.select_related(
                'can_ho', 'can_ho__chu_nha',
                'can_ho__toa_nha',
                'can_ho__toa_nha__district',
                'nhan_vien',
                'nhan_vien__tenant'
            ).prefetch_related(
                Prefetch(
                    'hdthue_set',
                    queryset=HDThue.objects.select_related('khach_thue').prefetch_related(
                        Prefetch(
                            'hd2dichvus_set',
                            queryset=HD2DichVus.objects.select_related('dich_vu').all(),
                            to_attr='list_service'
                        )
                    ).all(),
                    to_attr='hd_thues'
                )
            ).prefetch_related(
                Prefetch(
                    'hdmoigioi_set',
                    queryset=HDMoiGioi.objects.all(),
                    to_attr='hd_moi_giois'
                )
            ).prefetch_related(
                Prefetch(
                    'hddichvu_set',
                    queryset=HDDichVu.objects.all(),
                    to_attr='hd_dich_vus'
                )
            ).order_by('updated_at').all()
            return query

        def list(self, request, custom_queryset=None, custom_query_params=None, *args, **kwargs):
            pass

        def retrieve(self, request, custom_object=None, *args, **kwargs):
            pass

        def destroy(self, request, *args, **kwargs):
            pass

        def partial_update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
            try:
                obj = HDGroups.objects.get(pk=kwargs['pk'])
            except HDGroups.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().partial_update(request, custom_instance=obj, *args, **kwargs)

        def create(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            hg_group = serializer.save()

            general_response = rsp.Response(SubHDGroupResponseSerializer(hg_group).data).generate_response()
            response = Response(general_response, status=status.HTTP_201_CREATED)
            return response

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-hd-group')
        def list_hd_group(self, request, *args, **kwargs):
            search = self.request.GET.get("search", None)
            queryset = self.common_query()
            if search:
                queryset = queryset.filter(name__icontains=search)
            results = self.get_response_serializer(queryset, many=True).data
            return super().custom_response(results)

        @action(detail=True, permission_classes=[IsAuthenticated], methods=['get'], url_path='detail-hd-group')
        def detail_hd_group(self, request, *args, **kwargs):
            try:
                obj = self.common_query().get(pk=kwargs['pk'])
            except HDGroups.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().retrieve(request, custom_object=obj, *args, **kwargs)

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['post'], url_path='delete_hdgroup')
        def delete_multi(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            list_hdgroup = HDGroups.objects.filter(pk__in=serializer.validated_data['list_id'])
            hd_thue = HDThue.objects.filter(hd_group__in=list_hdgroup)
            hd_moigioi = HDMoiGioi.objects.filter(hd_group__in=list_hdgroup)
            HDDichVu.objects.filter(hd_group__in=list_hdgroup).delete()

            list_instance = HD2DichVus.objects.filter(hd_thue__in=hd_thue)
            list_hd_thue_id = hd_thue.values_list('pk', flat=True)
            list_hd_moigioi_id = hd_moigioi.values_list('pk', flat=True)

            ServiceTransactions.objects.filter(hd_2_dichvu__in=list_instance).delete()
            PaymentTransactions.objects.filter(
                Q(hop_dong_id__in=list_hd_thue_id,
                  hop_dong_type=ContentType.objects.get_for_model(HDThue).id) |
                Q(hop_dong_id__in=list_hd_moigioi_id,
                  hop_dong_type=ContentType.objects.get_for_model(
                      HDMoiGioi).id)).delete()

            list_instance.delete()
            hd_thue.delete()
            hd_moigioi.delete()
            list_hdgroup.delete()

            return super().custom_response({})


class HDThueView:
    search_field = openapi.Parameter(
        'search',
        openapi.IN_QUERY,
        description="Tim kiem theo ten can ho",
        type=openapi.TYPE_STRING
    )

    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='contract_expired', decorator=swagger_auto_schema(
        manual_parameters=[search_field]
    ))
    class HDThueViewSet(GenericViewSet):
        permission_classes = [IsAdminRole]
        serializer_class = HDThueResponseSerializer
        queryset = HDThue.objects.all()
        action_serializers = {
            'contract_expired_response': HDThueExpiredResponseSerializer
        }

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

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='contract-expired')
        def contract_expired(self, request, *args, **kwargs):
            search = self.request.GET.get("search", None)
            query = HDThue.objects.annotate(
                now=Cast(timezone.now(), output_field=DateField())
            ).annotate(
                diff=ExpressionWrapper(F('end_date') - F('now'), output_field=DurationField())
            ).filter(diff__lte=datetime.timedelta(30)).select_related(
                'khach_thue', 'hd_group__can_ho',
                'hd_group__can_ho__chu_nha',
                'hd_group__can_ho__toa_nha',
                'hd_group__can_ho__toa_nha__district',
                'hd_group'
            )
            if search:
                query = query.filter(hd_group__can_ho__name__icontains=search)
            results = HDThueExpiredResponseSerializer(query, many=True).data
            return super().custom_response(results)
