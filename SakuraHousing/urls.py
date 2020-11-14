"""SakuraHousing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from apps.authentication.urls import urlpatterns as auth_urlpatterns
from apps.common.urls import urlpatterns as common_urlpatterns
from apps.contract.urls import urlpatterns as contract_urlpatterns

schema_view = get_schema_view(
    openapi.Info(
        title="HapinessBook API",
        default_version='v1',
        description="Document of HapinessBook nurse API",
        contact=openapi.Contact(email="dung.nguyenviet@mor.com.vn"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
    #     name='schema-json'),
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^silk/', include('silk.urls', namespace='silk')),
]

urlpatterns += auth_urlpatterns
urlpatterns += common_urlpatterns
urlpatterns += contract_urlpatterns
