from django.db import models
# from django.contrib import admin
# from django.conf import settings
from django.contrib.auth.models import User
import random


def random_int():
    return str(random.randint(10000, 99999))


class Goat(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    is_inside = models.BooleanField(auto_created=True, default=False)
    cold_protection = models.IntegerField(default=random_int)


class GoatToUser(models.Model):
    goat = models.ForeignKey(Goat, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)