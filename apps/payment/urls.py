from apps.payment.versions.v1.router import payment_urlpatterns

from django.urls import path, include

urlpatterns = [
    path('payment/', include(payment_urlpatterns)),

]
