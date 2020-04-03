from django.shortcuts import render
from django.http import HttpResponse
import datetime
import requests
from .models import WeatherDataHourly, GeoData

import logging

logger = logging.getLogger(__name__)

def index(request):
    now = datetime.datetime.now()
    html = "<html><body>The time is now %s." % now
    html += "<br>"
    html += "</body></html>"
    return HttpResponse(html)


def list_weather(request):

    if not check_location_data(request):
        user_geodata = get_user_geodata(request)
    else:
        user_geodata = get_old_user_geodata(request)

    weather_data = get_weather_data(user_geodata)

    if WeatherDataHourly.objects.filter(geo_data_id=user_geodata.id):
        WeatherDataHourly.objects.filter(geo_data_id=user_geodata.id).delete()
    save_weather_data(user_geodata, weather_data)

    data = WeatherDataHourly.objects.filter(geo_data_id=user_geodata.id)

    logger.error(data)

    return render(request, 'weather.html', {'geodata': user_geodata,
                                            'weather_data': data})


def save_weather_data(geodata, weather_data):

    for data in weather_data['list']:
        temp_c = data['main']['temp'] - 273.15
        feels_like_c = data['main']['feels_like'] - 273.15
        entry = WeatherDataHourly(geo_data_id=geodata.id,
                                  time=data['dt_txt'],
                                  temp=temp_c,
                                  feels_like=feels_like_c,
                                  weather_str=data['weather'][0]['description'],
                                  wind=data['wind']['speed'])
        entry.save()


def get_user_geodata(request):
    response = requests.get('http://api.ipstack.com/check?access_key=8c902a4d5fd93242e3d7f39f731b82bf')
    geo_data = response.json()

    geodata_entry = GeoData(user_id=request.user.id,
                            city=geo_data['city'],
                            country=geo_data['country_name'],
                            lat=geo_data['latitude'],
                            lon=geo_data['longitude'])
    geodata_entry.save()
    return geodata_entry


def get_weather_data(user_geodata):
    api_key = '0aaa134f5c8dec6649a74fb386d02270'  # 'd9bf72db25eb40e64cee72836e1e1f26'
    lat = str(round(user_geodata.lat))
    lon = str(round(user_geodata.lon))
    request_url = 'http://api.openweathermap.org/data/2.5/forecast?lat=' + lat + \
                  '&lon=' + lon + '&appid=' + api_key
    weather_response = requests.get(request_url)
    return weather_response.json()


def get_old_user_geodata(request):
    return GeoData.objects.get(user_id=request.user.id)


def check_location_data(request):
    if not GeoData.objects.filter(user_id=request.user.id):
        return False
    return True

