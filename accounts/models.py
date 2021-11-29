from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    kakao_id = models.PositiveIntegerField(blank=True)
