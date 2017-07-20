from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.core.exceptions import ValidationError
import uuid
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email,
            password = password,
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class MyUser(AbstractBaseUser):
    username = models.CharField( max_length = 20, unique = True )
    first_name = models.CharField( max_length = 100 )
    last_name = models.CharField( max_length= 100 )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique = True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    token = models.CharField(max_length=64)
    expiry = models.DateTimeField(default=datetime.datetime.now, blank=True)
 #   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

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