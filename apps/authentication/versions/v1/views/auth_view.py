from datetime import datetime

# Create your views here.
from django.utils.decorators import method_decorator
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
    AccountCreateSerializer, TenantRequestSerializer, AccountRequestSerializer
from apps.authentication.versions.v1.serializers.response_serializer import UserResponseSerializer, \
    TenantResponseSerializer
from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException
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
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class TenantViewSet(GenericViewSet):
        serializer_class = TenantRequestSerializer
        queryset = Tenants.objects.all()
        action_serializers = {
            'create_request': TenantRequestSerializer,
            'list_tenant_response': TenantResponseSerializer,
            'partial_update_response': TenantResponseSerializer,
            'detail_tenant_response': TenantResponseSerializer
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
            results = self.get_response_serializer(query, many=True).data
            return super().custom_response(results)
        
        @action(detail=True, permission_classes=[IsAuthenticated], methods=['get'], url_path='detail-tenant')
        def detail_tenant(self, request, *args, **kwargs):
            try:
                obj = Tenants.objects.get(pk=kwargs['pk'])
            except Tenants.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().retrieve(request, custom_object=obj, *args, **kwargs)


class AccountView:
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    # @method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class AccountViewSet(GenericViewSet):
        serializer_class = AccountRequestSerializer
        queryset = Accounts.objects.all()
        action_serializers = {
            'list_account_response': UserResponseSerializer,
            'partial_update_response': UserResponseSerializer,
        }
        permission_classes = [IsAdminRole]
        
        def retrieve(self, request, custom_object=None, *args, **kwargs):
            pass
        
        def destroy(self, request, *args, **kwargs):
            pass
        
        def partial_update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
            try:
                obj = Accounts.objects.get(pk=kwargs['pk'])
            except Tenants.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().partial_update(request, custom_instance=obj, *args, **kwargs)
        
        def create(self, request, *args, **kwargs):
            pass
        
        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-account')
        def list_account(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)
