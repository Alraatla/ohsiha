import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class GeoData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    lat = models.DecimalField(default=0, decimal_places=1, max_digits=4)
    lon = models.DecimalField(default=0, decimal_places=1, max_digits=4)


class WeatherDataHourly(models.Model):
    geo_data = models.ForeignKey(GeoData, on_delete=models.CASCADE, null=True)
    time = models.CharField(max_length=100)
    temp = models.IntegerField(default=0)
    feels_like = models.IntegerField(default=0)
    weather_str = models.CharField(max_length=100)
    wind = models.DecimalField(decimal_places=1, max_digits=4)




# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#     def __str__(self):
#         return self.question_text
#
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#     def __str__(self):
#         return self.choice_text
