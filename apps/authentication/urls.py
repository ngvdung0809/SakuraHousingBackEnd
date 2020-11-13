from apps.authentication.versions.v1.router import auth_urlpatterns, tenant_urlpatterns

from django.urls import path, include

urlpatterns = [
    path('auth/', include(auth_urlpatterns)),
    path('tenant/', include(tenant_urlpatterns)),
]
