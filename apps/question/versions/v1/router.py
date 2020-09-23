from django.conf.urls import url

from apps.authentication.versions.v1.views import auth_view

auth_urlpatterns = [
    url(r'v1/login/$', auth_view.AuthenticationViewSet.as_view()),
    # url(r'v1/logout/$', auth_view.LogoutViewSet.as_view()),
]
