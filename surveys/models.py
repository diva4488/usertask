from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    ROLES = (
        ('admin', 'admin'),
        ('manager', 'manager'),
        ('internal User', 'internal User'),
    )
    role = models.CharField(max_length=100, choices=ROLES)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Custom related name to avoid conflicts
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Custom related name to avoid conflicts
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Survey(models.Model):
    name = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    owner = models.CharField(max_length=150)
    status = models.CharField(max_length=50, )
    
    def __str__(self):
        return self.name


class Log(models.Model):
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, related_name='logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"Log for {self.survey.name} at {self.timestamp}"