from django.contrib import admin
from apps.authentication.models import *

# Register your models here.
# Common
admin.site.register(User)
admin.site.register(Company)
admin.site.register(UserAuth)
