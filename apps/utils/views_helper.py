# Create your views here.
from rest_framework import viewsets, mixins, status, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import apps.utils.response_interface as rsp


class EmptySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass
    
    def create(self, validated_data):
        pass


class SerializerMixin(object):
    action_serializers = {}
    request_serializer_class = None
    response_serializer_class = None
    
    def get_request_serializer_class(self):
        if self.action + "_request" in self.action_serializers:
            return self.action_serializers.get(self.action + "_request", None)
        elif self.request_serializer_class:
            return self.request_serializer_class
        else:
            return self.serializer_class
    
    def get_response_serializer_class(self):
        if self.action + "_response" in self.action_serializers:
            return self.action_serializers.get(self.action + "_response", None)
        elif self.response_serializer_class:
            return self.response_serializer_class
        else:
            return self.serializer_class


class QuerySetMixin(object):
    action_query_sets = {}
    
    def get_queryset(self):
        if self.action in self.action_query_sets:
            return self.action_query_sets.get(self.action, None)
        else:
            return super().get_queryset()


class GenericViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet,
                     SerializerMixin,
                     QuerySetMixin,
                     ):
    # permission_classes = (IsAuthenticated | ReadOnly,)
    
    def perform_create(self, serializer):
        return serializer.save()
    
    def perform_update(self, serializer):
        return serializer.save()
    
    def get_request_serializer(self, *args, **kwargs):
        if self.get_request_serializer_class():
            serializer_class = self.get_request_serializer_class()
        else:
            serializer_class = self.serializer_class
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
    
    def get_response_serializer(self, *args, **kwargs):
        if self.get_response_serializer_class():
            serializer_class = self.get_response_serializer_class()
        else:
            serializer_class = self.serializer_class
        
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
    
    def get_serializer_class(self):
        serializer_class = self.get_request_serializer_class()
        if serializer_class is None:
            serializer_class = self.serializer_class
        if serializer_class is None:
            if not hasattr(self, "swagger_fake_view"):
                serializer_class = EmptySerializer
        return serializer_class
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        if isinstance(instance, (list,)):
            serializer = self.get_response_serializer(instance, many=True)
        else:
            serializer = self.get_response_serializer(instance)
        general_response = rsp.Response(serializer.data).generate_response()
        return Response(general_response, status=status.HTTP_201_CREATED)
    
    def list(self, request, custom_queryset=None, custom_query_params=None, *args, **kwargs):
        if not custom_queryset and not custom_queryset.__class__.__name__ == 'QuerySet':
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(custom_queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_response_serializer(page, many=True)
            general_response = rsp.Response(self.get_paginated_response(serializer.data).data).generate_response()
            if custom_query_params:
                data = self.get_data_from_response(general_response)
                general_response = self.apply_custom_query_params(general_response, data, custom_query_params)
            return Response(general_response, status=status.HTTP_200_OK)
        
        serializer = self.get_response_serializer(queryset, many=True)
        general_response = rsp.Response(serializer.data).generate_response()
        return Response(general_response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, custom_object=None, *args, **kwargs):
        if not custom_object and custom_object.__class__.__name__ == 'NoneType':
            instance = self.get_object()
        else:
            instance = custom_object
        
        serializer = self.get_response_serializer(instance)
        general_response = rsp.Response(serializer.data).generate_response()
        return Response(general_response, status=status.HTTP_200_OK)
    
    def update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
        if custom_instance:
            instance = custom_instance
        else:
            instance = self.get_object()
        partial = kwargs.pop('partial', False)
        if custom_data:
            serializer = self.get_request_serializer(instance, data=custom_data, partial=partial)
        else:
            serializer = self.get_request_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance_res = self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        serializer = self.get_response_serializer(instance_res)
        general_response = rsp.Response(serializer.data).generate_response()
        return Response(general_response, status=status.HTTP_200_OK)
    
    def partial_update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, custom_instance=custom_instance, custom_data=custom_data, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        general_response = rsp.Response(None).generate_response()
        return Response(general_response, status=status.HTTP_200_OK)
    
    def custom_response(self, data):
        general_response = rsp.Response(data).generate_response()
        return Response(general_response, status=status.HTTP_200_OK)
    
    def apply_custom_query_params(self, response, data, query_params):
        raise Exception('implementation needed')
    
    def get_data_from_response(self, response):
        if 'count' in response.get('data'):
            data = response.get('data').get('results')
        else:
            data = response.get('data')
        
        return data
    
    def set_data_to_response(self, response, data):
        if 'count' in response.get('data'):
            response['data']['results'] = data
        else:
            response['data'] = data
        return response
