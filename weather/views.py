from django.shortcuts import render
import os
from dotenv import load_dotenv
import requests
from .models import City
from .forms import CityForm
weather = os.path.expanduser('./weather')
load_dotenv(os.path.join(weather, 'keys.py'))
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}units=imperial&appid={OPENWEATHER_API_KEY}'
    cities = City.objects.all()
    # print(cities[1])
    # city = "Chicago"

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        print(city_weather)
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
            }
        weather_data.append(weather)
    # print(weather)
    context = {'weather_data': weather_data, 'form' : form }
    return render(request, 'weather/index.html', context)
