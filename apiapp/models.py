import datetime

from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class GeoData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    # country = models.CharField(max_length=100)
    country = CountryField(default='FI')
    lat = models.DecimalField(default=0, decimal_places=1, max_digits=4)
    lon = models.DecimalField(default=0, decimal_places=1, max_digits=4)


class WeatherDataHourly(models.Model):
    geo_data = models.ForeignKey(GeoData, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=100, default="16.4.2020")
    time = models.CharField(max_length=100, default="00:00:00")
    temp = models.IntegerField(default=0)
    feels_like = models.IntegerField(default=0)
    weather_str = models.CharField(max_length=100)
    wind = models.DecimalField(decimal_places=1, max_digits=4)
    icon = models.CharField(max_length=3, default='10d')

