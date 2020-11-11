from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from apps.utils.constants import GenderType


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('must have an email address.')
        usuario = self.model(email=self.normalize_email(email), username=username)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario
    
    def create_superuser(self, username, email, password):
        usuario = self.create_user(email=email, username=username, password=password)
        usuario.is_active = True
        usuario.is_admin = True
        usuario.save(using=self._db)
        return usuario


CHOICE_GENDER = (
    (GenderType.MALE.value, "Male"),
    (GenderType.FEMALE.value, "Female"),
    (GenderType.OTHER.value, "Other"),
)


class Company(models.Model):
    company_code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    company_type = models.IntegerField()
    unlock_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    
    class Meta:
        db_table = 'company'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.name)


class Accounts(AbstractBaseUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.IntegerField(choices=CHOICE_GENDER, default=GenderType.MALE.value)
    birthday = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'accounts'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.username)
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserAuth(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    auth_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_auth'
    
    def __str__(self):
        return '{}-{}'.format(self.id, self.auth_code)


class Token(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'token'
    
    def __str__(self):
        return "{} - {} - {}".format(self.id, self.user_id, self.token)
