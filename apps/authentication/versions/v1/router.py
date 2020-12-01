from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from apps.authentication.versions.v1.views import auth_view

router_auth = DefaultRouter()
router_auth.register(r'v1/register', auth_view.UserCreateView.UserCreateViewSet)
router_auth.register(r'v1/', auth_view.ChangePassWordView.ChangePassWordViewSet)

auth_urlpatterns = [
    url(r'v1/login/$', auth_view.AuthenticationView.AuthenticationViewSet.as_view()),
    url(r'v1/logout/$', auth_view.LogoutViewSet.as_view()),
]

router_tenant = DefaultRouter()
router_tenant.register(r'v1', auth_view.TenantView.TenantViewSet)

auth_urlpatterns += router_auth.urls

tenant_urlpatterns = []
tenant_urlpatterns += router_tenant.urls

router_account = DefaultRouter()
router_account.register(r'v1', auth_view.AccountView.AccountViewSet)

account_urlpatterns = []
account_urlpatterns += router_account.urls
