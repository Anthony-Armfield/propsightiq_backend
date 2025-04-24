from django.shortcuts import render
from .utils import get_weather_forecast

def home_view(request):
    """
    Home view that fetches and displays weather forecast
    """
    weather_data = get_weather_forecast()
    context = {
        'weather': weather_data,
        'page_title': 'PropSightIQ - Weather Forecast'
    }
    return render(request, 'weather/home.html', context)
