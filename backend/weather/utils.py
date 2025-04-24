import requests
from bs4 import BeautifulSoup
import logging
from decouple import config

logger = logging.getLogger(__name__)

def get_weather_forecast(location: str):
    """
    Given a location string, geocode it and fetch weather forecast from NWS
    """
    try:
        headers = {
            "User-Agent": config("GEOCODING_USER_AGENT")
        }
        # Use OpenStreetMap Nominatim API for geocoding
        geo_resp = requests.get(f"https://nominatim.openstreetmap.org/search",
                                params={"q": location, "format": "json"},
                                headers=headers,
                                timeout=10)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        if not geo_data:
            return {"success": False, "error": "Location not found."}

        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        # Use NWS API to get the forecast URL
        points_url = f"https://api.weather.gov/points/{lat},{lon}"
        points_resp = requests.get(points_url, timeout=10)
        points_resp.raise_for_status()
        forecast_page_url = points_resp.json()['properties']['forecast']

        # Debug
        print("Scraping URL:", forecast_page_url)

        forecast_resp = requests.get(forecast_page_url, timeout=10)
        forecast_resp.raise_for_status()
        forecast_data = forecast_resp.json()

        # Get grid data for detailed conditions
        grid_url = points_resp.json()['properties']['forecastGridData']
        grid_resp = requests.get(grid_url, timeout=10)
        grid_resp.raise_for_status()
        grid_data = grid_resp.json()

        temp_c = grid_data['properties']['temperature']['values'][0]['value']
        dew_c = grid_data['properties']['dewpoint']['values'][0]['value']
        wind_kmh = grid_data['properties']['windSpeed']['values'][0]['value']
        humidity = grid_data['properties']['relativeHumidity']['values'][0]['value']
        precip = grid_data['properties']['probabilityOfPrecipitation']['values'][0]['value']

        # Extract some useful values (all are time-series arrays)
        detailed = {
            "Temperature": f"{c_to_f(temp_c)}°F" if temp_c is not None else "N/A",
            "Dewpoint": f"{c_to_f(dew_c)}°F" if dew_c is not None else "N/A",
            "Wind Speed": f"{kmh_to_mph(wind_kmh)} mph" if wind_kmh is not None else "N/A",
            "Humidity": f"{humidity}%" if humidity is not None else "N/A",
            "Chance of Rain": f"{precip}%" if precip is not None else "N/A"
        }

        forecast_items = []
        for period in forecast_data["properties"]["periods"][:7]:
            forecast_items.append({
                "period": period["name"],
                "description": period["shortForecast"],
                "temperature": f"{period['temperature']}°{period['temperatureUnit']}"
            })
        location_name = location

        return {
            'location': location_name,
            'forecast': forecast_items,
            'detailed_conditions': detailed,
            'success': True
        }

    except Exception as e:
        logger.error(f"Error fetching weather for '{location}': {str(e)}")
        return {'success': False, 'error': str(e)}

        
def c_to_f(celsius):
    return round((celsius * 9/5) + 32)

def kmh_to_mph(kmh):
    return round(kmh * 0.621371)
