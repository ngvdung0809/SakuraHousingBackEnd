from apps.contract.versions.v1.router import hd_group_urlpatterns

from django.urls import path, include

urlpatterns = [
    path('hd-groups/', include(hd_group_urlpatterns)),
]
