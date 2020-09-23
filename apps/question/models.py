from django.db.models import JSONField
from django.db import models

# Create your models here.
from apps.utils.constants import Part

CHOICE_PART = (
    (Part.QUESTION_87.value, "87 questions"),
    (Part.QUESTION_7.value, "7 questions"),
)


class Section(models.Model):
    section_text = models.CharField(max_length=255)
    section_icon_family = models.CharField(max_length=255)
    section_icon = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    
    class Meta:
        db_table = 'section'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.section_text)


class QuestionType(models.Model):
    type = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'question_type'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.type)


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    part = models.IntegerField(choices=CHOICE_PART, default=Part.QUESTION_87.value)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    answer = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    
    class Meta:
        db_table = 'question'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.question_text)
