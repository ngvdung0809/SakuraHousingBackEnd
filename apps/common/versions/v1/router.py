from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from apps.common.versions.v1.views import common_view

toa_nha_urlpatterns = []
toa_nha_route = DefaultRouter()
toa_nha_route.register(r'v1', common_view.ToaNhaView.ToaNhaViewSet)
toa_nha_urlpatterns += toa_nha_route.urls

chu_nha_urlpatterns = []
chu_nha_route = DefaultRouter()
chu_nha_route.register(r'v1', common_view.ChuNhaView.ChuNhaViewSet)
chu_nha_urlpatterns += chu_nha_route.urls

khach_thue_urlpatterns = []
khach_thue_route = DefaultRouter()
khach_thue_route.register(r'v1', common_view.KhachThueView.KhachThueViewSet)
khach_thue_urlpatterns += khach_thue_route.urls

can_ho_urlpatterns = []
can_ho_route = DefaultRouter()
can_ho_route.register(r'v1', common_view.CanHoView.CanHoViewSet)
can_ho_urlpatterns += can_ho_route.urls

dich_vu_urlpatterns = []
dich_vu_route = DefaultRouter()
dich_vu_route.register(r'v1', common_view.DichVuView.DichVuViewSet)
dich_vu_urlpatterns += dich_vu_route.urls
