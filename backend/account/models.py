from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.nickname}'