from apps.authentication.versions.v1.router import auth_urlpatterns, account_urlpatterns

from django.urls import path, include

urlpatterns = [
    path('auth/', include(auth_urlpatterns)),
    path('account/', include(account_urlpatterns)),
]
