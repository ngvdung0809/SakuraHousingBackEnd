from django.contrib import admin
from apps.question.models import *

# Register your models here.
admin.register(QuestionType)
admin.register(Section)
admin.register(Question)
