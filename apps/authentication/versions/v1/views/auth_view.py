from datetime import datetime

# Create your views here.
from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import JSONWebTokenAPIView

import apps.utils.response_interface as rsp
from apps.authentication.models import Token, Accounts, Tenants
from apps.authentication.utils.custom_auth import JWTToken
from apps.authentication.versions.v1.serializers.request_serializer import LoginSerializer, EmptySerializer, \
    AccountCreateSerializer, TenantRequestSerializer, AccountRequestSerializer, ChangePasswordSerializer
from apps.authentication.versions.v1.serializers.response_serializer import UserResponseSerializer, \
    TenantResponseSerializer, DistrictResponseSerializer
from apps.common.models import ChuNhas, KhachThues, CanHos, ToaNhas, Districts
from apps.contract.models import HDGroups, HDThue, HDMoiGioi, HDDichVu
from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException
from apps.utils.multi_delete import MultiDeleteRequestSerializer
from apps.utils.permission import IsAdminRole
from apps.utils.views_helper import GenericViewSet


class AuthenticationView:
    # @method_decorator(name='post', decorator=swagger_auto_schema(
    #     responses={200: LoginSchemaResponseSerializer()}
    # ))
    class AuthenticationViewSet(JSONWebTokenAPIView):
        serializer_class = LoginSerializer

        def post(self, request, *args, **kwargs):
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data
                time_token = int(datetime.timestamp(datetime.utcnow()))
                Token.objects.create(user=user, token=time_token)
                return JWTToken(user, time_token).make_token(status=status.HTTP_200_OK)
            else:
                raise AuthenticationFailed


#
#
class LogoutViewSet(APIView):
    serializer_class = EmptySerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = request.auth.token
        Token.objects.filter(user=request.user, token=token).delete()
        general_response = rsp.Response(None).generate_response()
        return Response(general_response, status=status.HTTP_200_OK)


class UserCreateView:
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    # @method_decorator(name='create', decorator=swagger_auto_schema(
    #     responses={201: LoginSchemaResponseSerializer()}
    # ))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class UserCreateViewSet(GenericViewSet):
        serializer_class = AccountCreateSerializer
        queryset = Accounts.objects.select_related('tenant').all()

        # permission_classes = [IsAdminRole]

        def list(self, request, custom_queryset=None, custom_query_params=None, *args, **kwargs):
            pass

        def retrieve(self, request, custom_object=None, *args, **kwargs):
            pass

        def destroy(self, request, *args, **kwargs):
            pass

        def update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
            pass

        def partial_update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
            pass

        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            instance = self.perform_create(serializer)

            general_response = rsp.Response(UserResponseSerializer(instance).data).generate_response()
            response = Response(general_response, status=status.HTTP_201_CREATED)
            return response


class TenantView:
    search_field = openapi.Parameter(
        'search',
        openapi.IN_QUERY,
        description="Tim kiem theo ten toa nha",
        type=openapi.TYPE_STRING
    )

    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list_tenant', decorator=swagger_auto_schema(
        manual_parameters=[search_field]
    ))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class TenantViewSet(GenericViewSet):
        serializer_class = TenantRequestSerializer
        queryset = Tenants.objects.all()
        action_serializers = {
            'create_request': TenantRequestSerializer,
            'list_tenant_response': TenantResponseSerializer,
            'partial_update_response': TenantResponseSerializer,
            'detail_tenant_response': TenantResponseSerializer,
            'delete_multi_request': MultiDeleteRequestSerializer
        }
        permission_classes = [IsAdminRole]

        def list(self, request, custom_queryset=None, custom_query_params=None, *args, **kwargs):
            pass

        def retrieve(self, request, custom_object=None, *args, **kwargs):
            pass

        def destroy(self, request, *args, **kwargs):
            pass

        def partial_update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
            try:
                obj = Tenants.objects.get(pk=kwargs['pk'])
            except Tenants.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().partial_update(request, custom_instance=obj, *args, **kwargs)

        def create(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            tenant = serializer.save()

            general_response = rsp.Response(TenantResponseSerializer(tenant).data).generate_response()
            response = Response(general_response, status=status.HTTP_201_CREATED)
            return response

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-tenant')
        def list_tenant(self, request, *args, **kwargs):
            query = Tenants.objects.all()
            search = self.request.GET.get("search", None)
            if search:
                query = query.filter(
                    Q(name__icontains=search) |
                    Q(address__icontains=search)
                )
            results = self.get_response_serializer(query, many=True).data
            return super().custom_response(results)

        @action(detail=True, permission_classes=[IsAuthenticated], methods=['get'], url_path='detail-tenant')
        def detail_tenant(self, request, *args, **kwargs):
            try:
                obj = Tenants.objects.get(pk=kwargs['pk'])
            except Tenants.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().retrieve(request, custom_object=obj, *args, **kwargs)

        @action(detail=False, permission_classes=[IsAdminRole], methods=['post'], url_path='delete-tenant')
        def delete_multi(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = Tenants.objects.filter(pk__in=serializer.validated_data['list_id'])
            count = Accounts.objects.filter(tenant__in=obj).count()
            if count > 0:
                raise CustomException(ErrorCode.cant_delete_tenant)
            obj.delete()
            return super().custom_response({})


class AccountView:
    search_field = openapi.Parameter(
        'search',
        openapi.IN_QUERY,
        description="Tim kiem theo ten toa nha",
        type=openapi.TYPE_STRING
    )

    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    # @method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list_account', decorator=swagger_auto_schema(
        manual_parameters=[search_field]
    ))
    class AccountViewSet(GenericViewSet):
        serializer_class = AccountRequestSerializer
        queryset = Accounts.objects.order_by('updated_at').all()
        action_serializers = {
            'list_account_response': UserResponseSerializer,
            'partial_update_response': UserResponseSerializer,
            'delete_multi_request': MultiDeleteRequestSerializer
        }
        permission_classes = [IsAdminRole]

        def retrieve(self, request, custom_object=None, *args, **kwargs):
            pass

        def destroy(self, request, *args, **kwargs):
            pass

        def partial_update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
            try:
                obj = Accounts.objects.get(pk=kwargs['pk'])
            except Accounts.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().partial_update(request, custom_instance=obj, *args, **kwargs)

        def create(self, request, *args, **kwargs):
            pass

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-account')
        def list_account(self, request, *args, **kwargs):
            search = self.request.GET.get("search", None)
            if search:
                self.queryset = self.queryset.filter(
                    Q(username__icontains=search) |
                    Q(full_name__icontains=search)
                )
            return super().list(request, *args, **kwargs)

        @action(detail=False, permission_classes=[IsAdminRole], methods=['post'], url_path='delete_account')
        def delete_multi(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = Accounts.objects.filter(pk__in=serializer.validated_data['list_id'])
            if HDGroups.objects.filter(
                    Q(nhan_vien__in=obj) |
                    Q(created_by__in=obj) |
                    Q(updated_by__in=obj)
            ).count() > 0:
                raise CustomException(ErrorCode.cant_delete_account)
            obj.delete()

            return super().custom_response({})

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='overview')
        def overview(self, request, *args, **kwargs):
            count_account = Accounts.objects.count()
            count_chu_nha = ChuNhas.objects.count()
            count_khach_thue = KhachThues.objects.count()
            count_can_ho = CanHos.objects.count()
            count_toa_nha = ToaNhas.objects.count()
            count_hd_thue = HDThue.objects.count()
            count_hd_moi_gioi = HDMoiGioi.objects.count()
            count_hd_dich_vu = HDDichVu.objects.count()
            response = {
                'chu_nha': count_chu_nha,
                'khach_thue': count_khach_thue,
                'can_ho': count_can_ho,
                'toa_nha': count_toa_nha,
                'hd_thue': count_hd_thue,
                'hd_moi_gioi': count_hd_moi_gioi,
                'hd_dich_vu': count_hd_dich_vu,
                'chart_series1': [count_account, count_chu_nha, count_khach_thue, count_toa_nha, count_can_ho],
                'chart_series2': [count_hd_thue, count_hd_moi_gioi, count_hd_dich_vu]
            }
            return super().custom_response(response)

        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-district')
        def list_district(self, request, *args, **kwargs):
            district = Districts.objects.all()
            res = DistrictResponseSerializer(district, many=True).data
            return super().custom_response(res)


class ChangePassWordView:
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class ChangePassWordViewSet(GenericViewSet):
        permission_classes = (IsAuthenticated,)
        serializer_class = ChangePasswordSerializer
        queryset = Accounts.objects.all()
        action_serializers = {
            'change_password_request': ChangePasswordSerializer
        }

        @action(detail=False, methods=['post'], url_path='change-password')
        def change_password(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            general_response = rsp.Response(None).generate_response()
            return Response(general_response, status=status.HTTP_200_OK)
