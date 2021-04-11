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
    cities = City.objects.all()
    # print(cities[1].name)
    # city = "Chicago"
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

# {'coord': {'lon': -93.2638, 'lat': 44.98},
# 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}],
# 'base': 'stations',
# 'main': {'temp': 47.32, 'feels_like': 42.21, 'temp_min': 45, 'temp_max': 50, 'pressure': 1002, 'humidity': 76},
# 'visibility': 10000,
# 'wind': {'speed': 11.5, 'deg': 350},
# 'clouds': {'all': 90},
# 'dt': 1618159846,
# 'sys': {'type': 1, 'id': 4984, 'country': 'US', 'sunrise': 1618140880, 'sunset': 1618188773},
# 'timezone': -18000,
# 'id': 5037649,
# 'name': 'Minneapolis',
# 'cod': 200}

    form = CityForm()
    weather_data = []
    for city in cities:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={OPENWEATHER_API_KEY}&units=imperial"
        city_weather = requests.get(url.format(city.name)).json()
        # print(city_weather['wind']['speed'])
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'wind': city_weather['wind']['speed'],
            'winddir': city_weather['wind']['deg'],
            'icon': city_weather['weather'][0]['icon']
            }
        weather_data.append(weather)
    # print(weather)
    context = {'weather_data': weather_data, 'form' : form }
    return render(request, 'weather/index.html', context)
