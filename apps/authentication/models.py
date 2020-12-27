from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from apps.utils.constants import RoleType


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('must have an username.')
        usuario = self.model(username=username)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, username, password):
        usuario = self.create_user(username=username, password=password)
        usuario.is_admin = True
        usuario.save(using=self._db)
        return usuario


CHOICE_ROLE = (
    (RoleType.ADMIN.value, "Admin"),
    (RoleType.VIEWER.value, "Viewer"),
    (RoleType.DISABLE.value, "Disable"),
)


class Tenants(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.CharField(max_length=512, null=True, blank=True)
    phone = models.CharField(max_length=255)
    phone2 = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255)
    email2 = models.CharField(max_length=255, null=True, blank=True)
    dkkd = models.CharField(max_length=255, null=True, blank=True)
    tax_code = models.CharField(max_length=255, null=True, blank=True)
    rep = models.CharField(max_length=255, null=True, blank=True)
    rep_role = models.CharField(max_length=512, null=True, blank=True)
    ten_tk = models.CharField(max_length=255, null=True, blank=True)
    so_TK = models.CharField(max_length=255, null=True, blank=True)
    chi_nhanh = models.CharField(max_length=255, null=True, blank=True)
    ngan_hang = models.CharField(max_length=255, null=True, blank=True)
    ten_tk2 = models.CharField(max_length=255, null=True, blank=True)
    so_TK2 = models.CharField(max_length=255, null=True, blank=True)
    chi_nhanh2 = models.CharField(max_length=255, null=True, blank=True)
    ngan_hang2 = models.CharField(max_length=255, null=True, blank=True)
    note = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        db_table = 'tenants'

    def __str__(self):
        return '{}-{}-{}'.format(self.id, self.name, self.address)


class Accounts(AbstractBaseUser):
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    role = models.IntegerField(choices=CHOICE_ROLE, default=RoleType.VIEWER.value)
    is_admin = models.BooleanField(default=False)
    staff_code = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']

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


class Token(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'token'

    def __str__(self):
        return "{} - {} - {}".format(self.id, self.user_id, self.token)
