from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from apps.contract.versions.v1.views import contract_view

hd_group_urlpatterns = []
hd_group_route = DefaultRouter()
hd_group_route.register(r'v1/hd-thue', contract_view.HDThueView.HDThueViewSet)
hd_group_route.register(r'v1', contract_view.HDGroupView.HDGroupViewSet)
hd_group_urlpatterns += hd_group_route.urls
