from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import apps.utils.response_interface as rsp
from apps.contract.models import HDGroups, HDThue, HDMoiGioi, HDDichVu
from apps.contract.versions.v1.serializers.request_serializer import HDGroupRequestSerializer, \
    HDMoiGioiRequestSerializer
from apps.contract.versions.v1.serializers.response_serializer import HDGroupResponseSerializer, \
    HDThueResponseSerializer, HDMoiGioiResponseSerializer, HDDichVuResponseSerializer
from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException
from apps.utils.views_helper import GenericViewSet


class HDGroupView:
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class HDGroupViewSet(GenericViewSet):
        serializer_class = HDGroupRequestSerializer
        queryset = HDGroups.objects.all()
        permission_classes = [IsAuthenticated]
        action_serializers = {
            'create_request': HDGroupRequestSerializer,
            'list_response': HDGroupResponseSerializer,
            'partial_update_response': HDGroupResponseSerializer,
            'retrieve_response': HDGroupResponseSerializer,
            # 'create_contract_request':
        }

        def list(self, request, custom_queryset=None, custom_query_params=None, *args, **kwargs):
            query = HDGroups.objects.select_related('can_ho', 'can_ho__chu_nha').all()
            results = self.get_response_serializer(query, many=True).data
            return super().custom_response(results)

        def retrieve(self, request, custom_object=None, *args, **kwargs):
            try:
                obj = HDGroups.objects.select_related('can_ho', 'can_ho__chu_nha').get(pk=kwargs['pk'])
            except HDGroups.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().retrieve(request, custom_object=obj, *args, **kwargs)

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

            general_response = rsp.Response(HDGroupResponseSerializer(hg_group).data).generate_response()
            response = Response(general_response, status=status.HTTP_201_CREATED)
            return response

        # @action(detail=False, methods=['post'], url_path='create-contract')
        # def create_contract(self, request, *args, **kwargs):
        #     pass


class HDThueView:
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class HDThueViewSet(GenericViewSet):
        serializer_class = HDThueResponseSerializer
        queryset = HDThue.objects.all()
        permission_classes = [IsAuthenticated]
        action_serializers = {
            # 'create_request': HDGroupRequestSerializer,
            'list_response': HDThueResponseSerializer,
            # 'partial_update_response': HDGroupResponseSerializer,
            # 'retrieve_response': HDGroupResponseSerializer,
        }

        def list(self, request, custom_queryset=None, custom_query_params=None, *args, **kwargs):
            query = HDThue.objects.select_related(
                'khach_thue',
                'hd_group__can_ho',
                'hd_group__can_ho__toa_nha',
                'hd_group__can_ho__chu_nha',
                'nhan_vien'

            ).all()
            results = self.get_response_serializer(query, many=True).data
            return super().custom_response(results)

        def retrieve(self, request, custom_object=None, *args, **kwargs):
            # try:
            #     obj = HDGroups.objects.select_related('can_ho', 'can_ho__chu_nha').get(pk=kwargs['pk'])
            # except HDGroups.DoesNotExist:
            #     raise CustomException(ErrorCode.not_found_record)
            # return super().retrieve(request, custom_object=obj, *args, **kwargs)
            pass

        def destroy(self, request, *args, **kwargs):
            pass

        def partial_update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
            # try:
            #     obj = HDGroups.objects.get(pk=kwargs['pk'])
            # except HDGroups.DoesNotExist:
            #     raise CustomException(ErrorCode.not_found_record)
            # return super().partial_update(request, custom_instance=obj, *args, **kwargs)
            pass

        def create(self, request, *args, **kwargs):
            # serializer = self.get_request_serializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            #
            # hg_group = serializer.save()
            #
            # general_response = rsp.Response(HDGroupResponseSerializer(hg_group).data).generate_response()
            # response = Response(general_response, status=status.HTTP_201_CREATED)
            # return response
            pass


class HDMoiGioiView:
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class HDMoiGioiViewSet(GenericViewSet):
        serializer_class = HDMoiGioiResponseSerializer
        queryset = HDMoiGioi.objects.all()
        permission_classes = [IsAuthenticated]
        action_serializers = {
            # 'create_request': HDGroupRequestSerializer,
            'list_response': HDMoiGioiResponseSerializer,
            'partial_update_response': HDMoiGioiResponseSerializer,
            'partial_update_request': HDMoiGioiRequestSerializer,
            'retrieve_response': HDMoiGioiResponseSerializer,
        }

        def list(self, request, custom_queryset=None, custom_query_params=None, *args, **kwargs):
            query = HDMoiGioi.objects.select_related(
                'hd_group__can_ho',
                'hd_group__can_ho__toa_nha',
                'hd_group__can_ho__chu_nha',
                'nhan_vien',
                'tenant'

            ).all()
            results = self.get_response_serializer(query, many=True).data
            return super().custom_response(results)

        def retrieve(self, request, custom_object=None, *args, **kwargs):
            try:
                obj = HDMoiGioi.objects.select_related(
                    'hd_group__can_ho',
                    'hd_group__can_ho__toa_nha',
                    'hd_group__can_ho__chu_nha',
                    'nhan_vien'
                ).get(pk=kwargs['pk'])
            except HDMoiGioi.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().retrieve(request, custom_object=obj, *args, **kwargs)

        def destroy(self, request, *args, **kwargs):
            pass

        def partial_update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
            try:
                obj = HDMoiGioi.objects.get(pk=kwargs['pk'])
            except HDGroups.DoesNotExist:
                raise CustomException(ErrorCode.not_found_record)
            return super().partial_update(request, custom_instance=obj, *args, **kwargs)

        def create(self, request, *args, **kwargs):
            # serializer = self.get_request_serializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            #
            # hg_group = serializer.save()
            #
            # general_response = rsp.Response(HDGroupResponseSerializer(hg_group).data).generate_response()
            # response = Response(general_response, status=status.HTTP_201_CREATED)
            # return response
            pass


class HDDichVuView:
    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
    @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
    class HDDichVuViewSet(GenericViewSet):
        serializer_class = HDDichVuResponseSerializer
        queryset = HDDichVu.objects.all()
        permission_classes = [IsAuthenticated]
        action_serializers = {
            # 'create_request': HDGroupRequestSerializer,
            'list_response': HDDichVuResponseSerializer,
            # 'partial_update_response': HDGroupResponseSerializer,
            # 'retrieve_response': HDGroupResponseSerializer,
        }

        def list(self, request, custom_queryset=None, custom_query_params=None, *args, **kwargs):
            query = HDDichVu.objects.select_related(
                'hd_group__can_ho',
                'hd_group__can_ho__toa_nha',
                'hd_group__can_ho__chu_nha',
                'nhan_vien',
                'tenant'

            ).all()
            results = self.get_response_serializer(query, many=True).data
            return super().custom_response(results)

        def retrieve(self, request, custom_object=None, *args, **kwargs):
            # try:
            #     obj = HDGroups.objects.select_related('can_ho', 'can_ho__chu_nha').get(pk=kwargs['pk'])
            # except HDGroups.DoesNotExist:
            #     raise CustomException(ErrorCode.not_found_record)
            # return super().retrieve(request, custom_object=obj, *args, **kwargs)
            pass

        def destroy(self, request, *args, **kwargs):
            pass

        def partial_update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
            # try:
            #     obj = HDGroups.objects.get(pk=kwargs['pk'])
            # except HDGroups.DoesNotExist:
            #     raise CustomException(ErrorCode.not_found_record)
            # return super().partial_update(request, custom_instance=obj, *args, **kwargs)
            pass

        def create(self, request, *args, **kwargs):
            # serializer = self.get_request_serializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            #
            # hg_group = serializer.save()
            #
            # general_response = rsp.Response(HDGroupResponseSerializer(hg_group).data).generate_response()
            # response = Response(general_response, status=status.HTTP_201_CREATED)
            # return response
            pass
