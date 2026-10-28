from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class RoleChoices(models.TextChoices):
    DEVELOPER='Developer','Developer'
    ADMIN='Admin','Admin'
    PROJECT_COORDINATOR='Project Coordinator','Project Coordinator'

class Profile(AbstractUser):
    role=models.CharField(max_length=20,choices=RoleChoices.choices)
    
    class Meta:
        verbose_name='Profiles'
        verbose_name_plural='Profiles'

    def __str__(self):
        return self.username