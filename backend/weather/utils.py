import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def get_weather_forecast():
    """
    Scrape weather forecast data from National Weather Service
    
    Returns:
        dict: Dictionary containing weather data or error message
    """
    url = "https://forecast.weather.gov/MapClick.php?x=210&y=159&site=boi&zmx=&zmy=&map_x=210&map_y=159"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get location
        location_elem = soup.find('h2', class_='panel-title')
        location = location_elem.text.strip() if location_elem else "Location Unavailable"
        
        # Get current conditions
        conditions = {}
        current_conditions = soup.find(id='current_conditions-summary')
        if current_conditions:
            temp_elem = current_conditions.find(class_='myforecast-current-lrg')
            conditions['temperature'] = temp_elem.text if temp_elem else "N/A"
            
            condition_elem = current_conditions.find(class_='myforecast-current')
            conditions['condition'] = condition_elem.text if condition_elem else "N/A"
        
        # Get detailed conditions
        detailed = {}
        detail_items = soup.find_all(class_='col-sm-2 forecast-label')
        for item in detail_items:
            label = item.text.strip().rstrip(':')
            value = item.find_next_sibling(class_='col-sm-10 forecast-value')
            if value:
                detailed[label] = value.text.strip()
        
        # Get forecast
        forecast_items = []
        forecast_divs = soup.select('.tombstone-container')
        
        for div in forecast_divs:
            period = div.find(class_='period-name')
            desc = div.find(class_='short-desc')
            temp = div.find(class_='temp')
            
            if period and desc and temp:
                forecast_items.append({
                    'period': period.text.strip(),
                    'description': desc.text.strip(),
                    'temperature': temp.text.strip()
                })
        
        weather_data = {
            'location': location,
            'current_conditions': conditions,
            'detailed_conditions': detailed,
            'forecast': forecast_items[:7],  # Limit to 7 days
            'success': True
        }
        
        return weather_data
    
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return {
            'success': False,
            'error': f"Could not retrieve weather information: {str(e)}"
        }
