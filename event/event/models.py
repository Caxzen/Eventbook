from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
# Create your models here.
class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

class Users(AbstractBaseUser):
    email=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    password=models.CharField(max_length=20)
    objects =  CustomUserManager()
    class Meta:
        app_label = 'event'