from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from apps.authentication.versions.v1.views import auth_view

# router_auth = DefaultRouter()
# router_auth.register(r'v1/register', auth_view.UserCreateView.UserCreateViewSet)

auth_urlpatterns = [
    url(r'v1/login/$', auth_view.AuthenticationView.AuthenticationViewSet.as_view()),
    # url(r'v1/logout/$', auth_view.LogoutViewSet.as_view()),
]

# account_auth = DefaultRouter()
# account_auth.register(r'v1/verify-account', auth_view.VerifyAccountView.VerifyAccountViewSet)
#
# auth_urlpatterns += router_auth.urls
#
# account_urlpatterns = []
# account_urlpatterns += account_auth.urls
