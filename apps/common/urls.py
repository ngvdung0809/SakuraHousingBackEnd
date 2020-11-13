from apps.common.versions.v1.router import toa_nha_urlpatterns, chu_nha_urlpatterns, khach_thue_urlpatterns, \
    can_ho_urlpatterns, dich_vu_urlpatterns

from django.urls import path, include

urlpatterns = [
    path('toa-nha/', include(toa_nha_urlpatterns)),
    path('chu-nha/', include(chu_nha_urlpatterns)),
    path('khach-thue/', include(khach_thue_urlpatterns)),
    path('can-ho/', include(can_ho_urlpatterns)),
    path('dich-vu/', include(dich_vu_urlpatterns)),
]
