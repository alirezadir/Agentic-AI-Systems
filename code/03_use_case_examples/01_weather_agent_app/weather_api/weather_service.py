import requests
from typing import Dict, Optional
from pydantic import BaseModel

class WeatherResponse(BaseModel):
    """Weather data model with type hints and validation."""
    temperature: float
    conditions: str
    location: str
    recommendation: Optional[str] = None

def get_simulated_weather(city: str) -> Optional[Dict]:
    """Get simulated weather data for testing."""
    simulated_data = {
        "San Francisco": {
            "temp": 65.0,
            "conditions": "Partly cloudy with fog"
        },
        "New York": {
            "temp": 75.0,
            "conditions": "Mostly sunny"
        },
        "London": {
            "temp": 60.0,
            "conditions": "Light rain"
        }
    }
    return simulated_data.get(city)

def get_weather_wttr(city: str) -> WeatherResponse:
    """Get weather from wttr.in API."""
    url = f"https://wttr.in/{city}?format=j1"
    
    print(f"fetching weather information from wttr.in API for city: {city}")
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    current = data['current_condition'][0]
    
    return WeatherResponse(
        temperature=float(current['temp_F']),
        conditions=current['weatherDesc'][0]['value'],
        location=city,
        recommendation=get_weather_recommendation(float(current['temp_F']), current['weatherDesc'][0]['value'])
    )

def get_weather_recommendation(temp: float, conditions: str) -> str:
    """Generate weather recommendations based on conditions."""
    conditions = conditions.lower()
    
    if "rain" in conditions or "shower" in conditions:
        return "Bring an umbrella and waterproof clothing!"
    elif "snow" in conditions:
        return "Dress warmly and wear snow boots!"
    elif "clear" in conditions and temp > 80:
        return "Hot and sunny - bring sunscreen and stay hydrated!"
    elif "clear" in conditions and temp < 50:
        return "Chilly but clear - bring a warm jacket!"
    else:
        return "Typical weather - dress comfortably for the temperature!"

def get_weather(city: str) -> WeatherResponse:
    """Main function to get weather data, trying simulated first then real API."""
    print(f"Getting weather information for city: {city}")
    # Try simulated data first
    data = get_simulated_weather(city)
    if data:
        return WeatherResponse(
            temperature=data["temp"],
            conditions=data["conditions"],
            location=city,
            recommendation=get_weather_recommendation(data["temp"], data["conditions"])
        )

    # If no simulated data, try real API
    try:
        return get_weather_wttr(city)
    except requests.RequestException as e:
        # In production, add proper error logging
        return WeatherResponse(
            temperature=0.0,
            conditions="Error fetching weather data",
            location=city,
            recommendation="Please try again later"
        ) 