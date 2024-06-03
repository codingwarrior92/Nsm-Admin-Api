from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        return

    def create_superuser(self, email, password=None, **extra_fields):
        # Perform your data insertion operations here
        user = {'email': email, 'password': make_password(password)}  
        user = User(**user)
        user.save()
        return

class User(AbstractUser, PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        related_name='authentication_user_set',  # Add related_name here
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='authentication_user_set',  # Add related_name here
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    email = models.EmailField(unique=True)
    password=models.TextField(max_length=50, unique=False, default="123123")
    username = models.CharField(max_length=50, unique=False, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    class Meta:
        db_table = 'users'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_joined = timezone.now()
        return super().save(*args, **kwargs)
  