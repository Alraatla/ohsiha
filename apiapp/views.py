from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
import requests
from .models import WeatherDataHourly, GeoData
from goats.models import Goat, GoatToUser
from .forms import GeoDataForm

import logging

logger = logging.getLogger(__name__)


def show_chart(request):
    goats = GoatToUser.objects.filter(owner_id=request.user)
    weather_data = WeatherDataHourly.objects.filter(geo_data_id=get_user_geodata(request).id)
    dates = []
    temps = []
    for hourly_data in weather_data:
        temps.append(str(hourly_data.temp))
        dates.append(change_date(hourly_data.date) + ' ' + hourly_data.time)
    data = []
    goats_in_list = []
    for goat in goats:
        # if goat.owner_id == request.user.id:
        goats_in_list.append(goat.goat)
    goats_in_list[0].cold_protection = 10000
    for goat in goats_in_list:
        data_list = []
        data_list.append(goat)
        goat_threshold = (-7) + ((goat.cold_protection-4500)/1000)/9
        for hourly in weather_data:
            data_list.append(str(int(hourly.temp+goat_threshold)))
        data.append(data_list)

    return render(request, 'weather_chart.html', {'dates': dates,
                                                  'data': data,
                                                  'temps': temps})


def list_weather(request):

    user_geodata = get_user_geodata(request)

    weather_data = get_weather_data(user_geodata)

    if WeatherDataHourly.objects.filter(geo_data_id=user_geodata.id):
        WeatherDataHourly.objects.filter(geo_data_id=user_geodata.id).delete()
    save_weather_data(user_geodata, weather_data)

    data = WeatherDataHourly.objects.filter(geo_data_id=user_geodata.id)

    return render(request, 'weather.html', {'geodata': user_geodata,
                                            'weather_data': data})


def save_weather_data(geodata, weather_data):

    for data in weather_data['list']:
        temp_c = data['main']['temp'] - 273.15
        feels_like_c = data['main']['feels_like'] - 273.15
        date, time = parse_time(data['dt_txt'])
        entry = WeatherDataHourly(geo_data_id=geodata.id,
                                  date=date,
                                  time=time,
                                  temp=temp_c,
                                  feels_like=feels_like_c,
                                  weather_str=data['weather'][0]['description'],
                                  wind=data['wind']['speed'],
                                  icon=data['weather'][0]['icon'])
        entry.save()


def get_user_geodata(request):

    if check_location_data(request):
        return get_old_user_geodata(request)
    else:
        response = requests.get('http://api.ipstack.com/check?access_key=8c902a4d5fd93242e3d7f39f731b82bf')
        geo_data = response.json()

        geodata_entry = GeoData(user_id=request.user.id,
                                city=geo_data['city'],
                                country=geo_data['country_code'],
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


def update_location(request):
    geo_data = GeoData.objects.get(user_id=request.user.id)
    form = GeoDataForm(request.POST or None, instance=geo_data)

    if form.is_valid():
        old_city = geo_data.city
        old_country = geo_data.country
        form.save()
        message = update_lon_lat(geo_data)
        if not message:
            return redirect('list_weather')
        else:
            geo_data.city = old_city
            geo_data.country = old_country
            geo_data.save()
            return render(request, 'geo_data-form.html', {'form': form, 'msg': message})
    return render(request, 'geo_data-form.html', {'form': form})


def update_lon_lat(geo_data):
    request_url = 'http://api.openweathermap.org/data/2.5/forecast?q=' + geo_data.city + ',' + str(geo_data.country.code) + \
        '&appid=0aaa134f5c8dec6649a74fb386d02270'
    response = requests.get(request_url).json()
    if response['cod'] == "200":
        geo_data.lat = response['city']['coord']['lat']
        geo_data.lon = response['city']['coord']['lon']
        geo_data.save()

    return response['message']


def parse_time(time):
    date_time = time.split(' ')
    date = date_time[0]
    time_parsed = date_time[1]
    year_month_day = date.split('-')
    year = year_month_day[0]
    month = year_month_day[1]
    day = year_month_day [2]
    date_corrected = day + "." + month + "." + year

    return date_corrected, time_parsed


def change_date(date):
    parsed = date.split('.')
    new_date = parsed[1] + '/' + parsed[0] + '/' + parsed[2][-2:]
    return new_date
