from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField
from django.db import models

# Create your models here.
from apps.authentication.models import User
from apps.utils.constants import GenderType


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    well_self_assessment = models.IntegerField()
    well_shd_assessment = models.IntegerField()
    well_gap_value = models.IntegerField()
    well_gap_message = models.IntegerField()
    balance_physical_self_assessment = models.IntegerField()
    balance_physical_shd_assessment = models.IntegerField()
    balance_mental_self_assessment = models.IntegerField()
    balance_mental_shd_assessment = models.IntegerField()
    balance_social_self_assessment = models.IntegerField()
    balance_social_shd_assessment = models.IntegerField()
    balance_message = models.IntegerField()
    condition_physical_bmi = models.IntegerField()
    condition_physical_abnormal = models.IntegerField()
    condition_physical_subjective_symptoms = models.IntegerField()
    condition_mental_regret = models.IntegerField()
    condition_mental_mood = models.IntegerField()
    condition_mental_fear = models.IntegerField()
    condition_mental_unstable = models.IntegerField()
    condition_mental_coherent = models.IntegerField()
    condition_social_family_score = models.IntegerField()
    condition_social_family_quality = models.IntegerField()
    condition_social_family_quantity = models.IntegerField()
    condition_social_friends_score = models.IntegerField()
    condition_social_friends_quality = models.IntegerField()
    condition_social_friends_quantity = models.IntegerField()
    condition_social_other_score = models.IntegerField()
    personality_feeling_nervous = models.IntegerField()
    personality_feeling_self_esteem = models.IntegerField()
    personality_feeling_kouchosei = models.IntegerField()
    personality_feeling_sokushinsyoten = models.IntegerField()
    personality_feeling_positive = models.IntegerField()
    personality_perception_think_type = models.IntegerField()
    personality_perception_option_type = models.IntegerField()
    personality_perception_detail_type = models.IntegerField()
    personality_perception_social_type = models.IntegerField()
    personality_decision_making_decision = models.IntegerField()
    personality_decision_making_sincerity = models.IntegerField()
    personality_decision_making_openness = models.IntegerField()
    personality_behavior_sociality = models.IntegerField()
    balance_score = models.IntegerField()
    personality_p6 = models.IntegerField()
    personality_p7 = models.IntegerField()
    personality_p9 = models.IntegerField()
    personality_p10 = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_data'
    
    def __str__(self):
        return self.id


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = JSONField()
    part = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    
    class Meta:
        db_table = 'user_answer'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.answer)
