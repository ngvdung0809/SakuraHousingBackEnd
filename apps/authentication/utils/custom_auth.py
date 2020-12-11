import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_encode_handler

import apps.utils.response_interface as rsp
from apps.authentication.models import Token
from apps.authentication.versions.v1.serializers.response_serializer import UserResponseSerializer
from apps.utils.constants import RoleType
from apps.utils.error_code import ErrorCode
from apps.utils.exception import CustomException


class CustomAuthentication(BaseAuthentication):
    authentication_header_prefix = 'JWT'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.authentication_header_prefix.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('invalid token')

        try:
            token = Token.objects.select_related('user').get(
                user_id=payload.get('user_id'), token=payload.get('time_create')
            )
            if token.user.role == RoleType.DISABLE.value:
                raise CustomException(ErrorCode.lock_account)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('not found token')
        return token.user, token


class JWTToken(object):
    def __init__(self, user, time_token):
        self.user = user
        self.token = time_token

    def make_token(self, status):
        payload = {
            'user_id': self.user.id,
            'time_create': self.token,
        }
        token = jwt_encode_handler(payload)
        profile = UserResponseSerializer(self.user).data
        response_data = {
            'token': token,
            'profile': profile
        }
        general_response = rsp.Response(response_data).generate_response()
        response = Response(general_response, status=status)
        return response
