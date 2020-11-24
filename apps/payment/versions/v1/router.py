from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from apps.payment.versions.v1.views import payment_view

payment_urlpatterns = []
payment_route = DefaultRouter()
payment_route.register(r'v1', payment_view.PaymentView.PaymentViewSet)
payment_urlpatterns += payment_route.urls
