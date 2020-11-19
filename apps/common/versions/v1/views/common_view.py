from django.utils.decorators import method_decorator
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
from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException
from apps.utils.permission import IsAdminRole
from apps.utils.views_helper import GenericViewSet


class ToaNhaView:
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class ToaNhaViewSet(GenericViewSet):
        serializer_class = ToaNhaRequestSerializer
        queryset = ToaNhas.objects.all()
        action_serializers = {
            'create_request': ToaNhaRequestSerializer,
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
            try:
                obj = ToaNhas.objects.get(pk=kwargs['pk'])
            except ToaNhas.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().partial_update(request, custom_instance=obj, *args, **kwargs)
        
        def create(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            toa_nha = serializer.save()
            
            general_response = rsp.Response(ToaNhaResponseSerializer(toa_nha).data).generate_response()
            response = Response(general_response, status=status.HTTP_201_CREATED)
            return response
        
        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-toa-nha')
        def list_toa_nha(self, request, *args, **kwargs):
            query = ToaNhas.objects.select_related('district').all()
            results = self.get_response_serializer(query, many=True).data
            return super().custom_response(results)
        
        @action(detail=True, permission_classes=[IsAuthenticated], methods=['get'], url_path='detail-toa-nha')
        def detail_toa_nha(self, request, *args, **kwargs):
            try:
                obj = ToaNhas.objects.select_related('district').get(pk=kwargs['pk'])
            except ToaNhas.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().retrieve(request, custom_object=obj, *args, **kwargs)


class ChuNhaView:
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class ChuNhaViewSet(GenericViewSet):
        serializer_class = ChuNhaRequestSerializer
        queryset = ToaNhas.objects.all()
        action_serializers = {
            'create_request': ChuNhaRequestSerializer,
            'list_toa_nha_response': ChuNhaResponseSerializer,
            'partial_update_response': ChuNhaResponseSerializer,
            'detail_chu_nha_response': ChuNhaResponseSerializer
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
                obj = ChuNhas.objects.get(pk=kwargs['pk'])
            except ChuNhas.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().partial_update(request, custom_instance=obj, *args, **kwargs)
        
        def create(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            chu_nha = serializer.save()
            
            general_response = rsp.Response(ChuNhaResponseSerializer(chu_nha).data).generate_response()
            response = Response(general_response, status=status.HTTP_201_CREATED)
            return response
        
        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-chu-nha')
        def list_chu_nha(self, request, *args, **kwargs):
            query = ChuNhas.objects.all()
            results = self.get_response_serializer(query, many=True).data
            return super().custom_response(results)
        
        @action(detail=True, permission_classes=[IsAuthenticated], methods=['get'], url_path='detail-chu-nha')
        def detail_chu_nha(self, request, *args, **kwargs):
            try:
                obj = ChuNhas.objects.get(pk=kwargs['pk'])
            except ChuNhas.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().retrieve(request, custom_object=obj, *args, **kwargs)


class KhachThueView:
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    class KhachThueViewSet(GenericViewSet):
        serializer_class = KhachThueRequestSerializer
        queryset = KhachThues.objects.all()
        action_serializers = {
            'create_request': KhachThueRequestSerializer,
            'list_khach_thue_response': KhachThueResponseSerializer,
            'partial_update_response': KhachThueResponseSerializer,
            'detail_khach_thue_response': KhachThueResponseSerializer
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
                obj = KhachThues.objects.get(pk=kwargs['pk'])
            except KhachThues.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().partial_update(request, custom_instance=obj, *args, **kwargs)
        
        def create(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            khach_thue = serializer.save()
            
            general_response = rsp.Response(KhachThueResponseSerializer(khach_thue).data).generate_response()
            response = Response(general_response, status=status.HTTP_201_CREATED)
            return response
        
        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-khach_thue')
        def list_khach_thue(self, request, *args, **kwargs):
            query = KhachThues.objects.all()
            results = self.get_response_serializer(query, many=True).data
            return super().custom_response(results)
        
        @action(detail=True, permission_classes=[IsAuthenticated], methods=['get'], url_path='detail-khach-thue')
        def detail_khach_thue(self, request, *args, **kwargs):
            try:
                obj = KhachThues.objects.get(pk=kwargs['pk'])
            except KhachThues.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().retrieve(request, custom_object=obj, *args, **kwargs)


class CanHoView:
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class CanHoViewSet(GenericViewSet):
        serializer_class = CanHoRequestSerializer
        queryset = CanHos.objects.all()
        action_serializers = {
            'create_request': CanHoRequestSerializer,
            'list_can_ho_response': CanHoResponseSerializer,
            'partial_update_response': CanHoResponseSerializer,
            'detail_can_ho_response': CanHoResponseSerializer
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
                obj = CanHos.objects.get(pk=kwargs['pk'])
            except CanHos.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().partial_update(request, custom_instance=obj, *args, **kwargs)
        
        def create(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            can_ho = serializer.save()
            
            general_response = rsp.Response(CanHoResponseSerializer(can_ho).data).generate_response()
            response = Response(general_response, status=status.HTTP_201_CREATED)
            return response
        
        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-can-ho')
        def list_can_ho(self, request, *args, **kwargs):
            query = CanHos.objects.select_related('chu_nha', 'toa_nha').all()
            results = self.get_response_serializer(query, many=True).data
            return super().custom_response(results)
        
        @action(detail=True, permission_classes=[IsAuthenticated], methods=['get'], url_path='detail-can-ho')
        def detail_can_ho(self, request, *args, **kwargs):
            try:
                obj = CanHos.objects.select_related('chu_nha', 'toa_nha').get(pk=kwargs['pk'])
            except CanHos.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().retrieve(request, custom_object=obj, *args, **kwargs)


class DichVuView:
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    class DichVuViewSet(GenericViewSet):
        serializer_class = DichVuRequestSerializer
        queryset = CanHos.objects.all()
        action_serializers = {
            'create_request': DichVuRequestSerializer,
            'list_dich_vu_response': DichVuResponseSerializer,
            'partial_update_response': DichVuResponseSerializer,
            'detail_dich_vu_response': DichVuResponseSerializer
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
                obj = DichVus.objects.get(pk=kwargs['pk'])
            except DichVus.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().partial_update(request, custom_instance=obj, *args, **kwargs)
        
        def create(self, request, *args, **kwargs):
            serializer = self.get_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            dich_vu = serializer.save()
            
            general_response = rsp.Response(DichVuResponseSerializer(dich_vu).data).generate_response()
            response = Response(general_response, status=status.HTTP_201_CREATED)
            return response
        
        @action(detail=False, permission_classes=[IsAuthenticated], methods=['get'], url_path='list-dich-vu')
        def list_dich_vu(self, request, *args, **kwargs):
            query = DichVus.objects.all()
            results = self.get_response_serializer(query, many=True).data
            return super().custom_response(results)
        
        @action(detail=True, permission_classes=[IsAuthenticated], methods=['get'], url_path='detail-dich-vu')
        def detail_dich_vu(self, request, *args, **kwargs):
            try:
                obj = DichVus.objects.get(pk=kwargs['pk'])
            except DichVus.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().retrieve(request, custom_object=obj, *args, **kwargs)
