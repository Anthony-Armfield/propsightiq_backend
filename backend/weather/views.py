from django.shortcuts import render
from .utils import get_weather_forecast

def home(request):
    weather_data = None
    error = None

    if request.method == "POST":
        user_location = request.POST.get("location")
        if user_location:
            result = get_weather_forecast(user_location)
            if result['success']:
                weather_data = result
            else:
                error = result['error']

    return render(request, "weather/home.html", {
        "weather": weather_data,
        "error": error,
    })
