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
# from apps.authentication.models import User, Token
from apps.authentication.models import Token
from apps.authentication.utils.custom_auth import JWTToken
# from apps.authentication.utils.send_email import EmailTemplate
# from apps.authentication.versions.v1.serializers.request_serializer import EmptySerializer, UserCreateSerializer, \
#     LoginSerializer, CheckEmailSerializer, CheckOTPCodeSerializer, CheckCompanySerializer
from apps.authentication.versions.v1.serializers.request_serializer import LoginSerializer
from apps.authentication.versions.v1.serializers.response_serializer import UserResponseSerializer
from apps.utils.views_helper import GenericViewSet


#


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
# class LogoutViewSet(APIView):
#     serializer_class = EmptySerializer
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, *args, **kwargs):
#         token = request.auth.token
#         Token.objects.filter(user=request.user, token=token).delete()
#         general_response = rsp.Response(None).generate_response()
#         return Response(general_response, status=status.HTTP_200_OK)
#
#
# class UserCreateView:
#     @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
#     # @method_decorator(name='create', decorator=swagger_auto_schema(
#     #     responses={201: LoginSchemaResponseSerializer()}
#     # ))
#     @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
#     @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
#     @method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
#     @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
#     class UserCreateViewSet(GenericViewSet):
#         serializer_class = UserCreateSerializer
#         queryset = User.objects.all()
#
#         def list(self, request, custom_queryset=None, custom_query_params=None, *args, **kwargs):
#             pass
#
#         def retrieve(self, request, custom_object=None, *args, **kwargs):
#             pass
#
#         def destroy(self, request, *args, **kwargs):
#             pass
#
#         def update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
#             pass
#
#         def partial_update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
#             pass
#
#         def create(self, request, *args, **kwargs):
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#
#             instance = self.perform_create(serializer)
#
#             mail_template = EmailTemplate()
#             mail_template.send_activation_email(instance)
#
#             general_response = rsp.Response(UserResponseSerializer(instance).data).generate_response()
#             response = Response(general_response, status=status.HTTP_201_CREATED)
#             return response
#
#
# class VerifyAccountView:
#     @method_decorator(name='list', decorator=swagger_auto_schema(auto_schema=None))
#     @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
#     @method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
#     @method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
#     @method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
#     @method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
#     class VerifyAccountViewSet(GenericViewSet):
#         serializer_class = CheckEmailSerializer
#         queryset = User.objects.all()
#         action_serializers = {
#             'check_exist_email_request': CheckEmailSerializer,
#             'check_exist_company_request': CheckCompanySerializer,
#             'check_auth_code_request': CheckOTPCodeSerializer
#         }
#
#         def list(self, request, custom_queryset=None, custom_query_params=None, *args, **kwargs):
#             pass
#
#         def retrieve(self, request, custom_object=None, *args, **kwargs):
#             pass
#
#         def destroy(self, request, *args, **kwargs):
#             pass
#
#         def update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
#             pass
#
#         def partial_update(self, request, custom_instance=None, custom_data=None, *args, **kwargs):
#             pass
#
#         def create(self, request, *args, **kwargs):
#             pass
#
#         @action(detail=False, methods=['post'], url_path='check-exist-email')
#         def check_exist_email(self, request, *args, **kwargs):
#             serializer = CheckEmailSerializer(data=request.data, **kwargs)
#             if serializer.is_valid(raise_exception=True):
#                 general_response = rsp.Response({}).generate_response()
#                 return Response(general_response, status=status.HTTP_200_OK)
#
#         @action(detail=False, methods=['post'], url_path='check-exist-company')
#         def check_exist_company(self, request, *args, **kwargs):
#             serializer = CheckCompanySerializer(data=request.data, **kwargs)
#             if serializer.is_valid(raise_exception=True):
#                 general_response = rsp.Response({}).generate_response()
#                 return Response(general_response, status=status.HTTP_200_OK)
#
#         @action(detail=False, methods=['post'], url_path='check-auth-code')
#         def check_auth_code(self, request, *args, **kwargs):
#             serializer = CheckOTPCodeSerializer(data=request.data, **kwargs)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 general_response = rsp.Response({}).generate_response()
#                 return Response(general_response, status=status.HTTP_200_OK)
