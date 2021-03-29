from django.shortcuts import render
import os
from dotenv import load_dotenv
import requests
weather = os.path.expanduser('./weather')
load_dotenv(os.path.join(weather, 'keys.py'))
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


# Create your views here.
def index(request):
    url = f"http://api.openweathermap.org/data/2.5/weather?q=las%20vegas&units=imperial&appid={OPENWEATHER_API_KEY}"
    city = 'Las Vegas'
    city_weather = requests.get(url.format(city)).json()
    # print(city_weather)
    weather = {
        'city': city,
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon']
    }
    # print(weather)
    return render(request, 'weather/index.html')
