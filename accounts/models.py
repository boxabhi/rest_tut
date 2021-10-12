from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    token = models.CharField(max_length=1000)
    is_active = models.BooleanField(default = False)