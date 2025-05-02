from flask import Flask, render_template, request, redirect, url_for
import requests
import os
import datetime

app = Flask(__name__)

# Air Quality Index (AQI) breakpoints for PM2.5 (in µg/m³)
PM25_AQI_BREAKPOINTS = [
    (0, 12.0, 'Good', 'aqi-good'),
    (12.1, 35.4, 'Moderate', 'aqi-moderate'),
    (35.5, 55.4, 'Unhealthy for Sensitive Groups', 'aqi-unhealthy-sensitive'),
    (55.5, 150.4, 'Unhealthy', 'aqi-unhealthy'),
    (150.5, 250.4, 'Very Unhealthy', 'aqi-very-unhealthy'),
    (250.5, float('inf'), 'Hazardous', 'aqi-hazardous')
]

# Air Quality Index (AQI) breakpoints for PM10 (in µg/m³)
PM10_AQI_BREAKPOINTS = [
    (0, 54, 'Good', 'aqi-good'),
    (55, 154, 'Moderate', 'aqi-moderate'),
    (155, 254, 'Unhealthy for Sensitive Groups', 'aqi-unhealthy-sensitive'),
    (255, 354, 'Unhealthy', 'aqi-unhealthy'),
    (355, 424, 'Very Unhealthy', 'aqi-very-unhealthy'),
    (425, float('inf'), 'Hazardous', 'aqi-hazardous')
]

# AQI breakpoints for Ozone (O3) in ppm
O3_AQI_BREAKPOINTS = [
    (0, 0.054, 'Good', 'aqi-good'),
    (0.055, 0.070, 'Moderate', 'aqi-moderate'),
    (0.071, 0.085, 'Unhealthy for Sensitive Groups', 'aqi-unhealthy-sensitive'),
    (0.086, 0.105, 'Unhealthy', 'aqi-unhealthy'),
    (0.106, 0.200, 'Very Unhealthy', 'aqi-very-unhealthy'),
    (0.201, float('inf'), 'Hazardous', 'aqi-hazardous')
]

def get_aqi_category(parameter, value):
    """Determine AQI category based on parameter and value."""
    if value is None:
        return None
    
    if parameter.lower() == 'pm25':
        breakpoints = PM25_AQI_BREAKPOINTS
    elif parameter.lower() == 'pm10':
        breakpoints = PM10_AQI_BREAKPOINTS
    elif parameter.lower() == 'o3':
        breakpoints = O3_AQI_BREAKPOINTS
    else:
        return None
    
    for low, high, category, css_class in breakpoints:
        if low <= value <= high:
            return {'category': category, 'css_class': css_class}
    
    return None

# OpenAQ API Key
API_KEY = "f68b9b4b6bcab3293b00b1d1a0fc95f84198c5f48d432dafd70735a3ef4ebd71"


@app.route('/')
def index():
    """Home page with location selection."""
    return render_template('index.html')

def get_latest_measurement(sensor_id):
    """Fetch the latest measurement for a specific sensor."""
    try:
        url = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements"
        headers = {"X-API-Key": API_KEY}
        params = {
            "limit": 1,  # Get only the latest measurement
            "sort": "desc"  # Sort by date in descending order
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("results") and len(data["results"]) > 0:
            return data["results"][0]
        else:
            return None
    except Exception:
        return None

@app.route('/location/<int:location_id>')
def location_details(location_id):
    """Display air quality information for the selected location."""
    try:
        # API request to OpenAQ for location info
        url = f"https://api.openaq.org/v3/locations/{location_id}"
        headers = {"X-API-Key": API_KEY}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        # Check if results are available
        if not data.get("results"):
            return render_template('error.html', message="No data found for this location.")
        
        location_data = data["results"][0]
        
        # Fetch the latest measurement for each sensor
        if location_data.get("sensors"):
            for sensor in location_data["sensors"]:
                sensor["latest_measurement"] = get_latest_measurement(sensor["id"])
                
                # Add AQI category if applicable
                if sensor["latest_measurement"] and "value" in sensor["latest_measurement"]:
                    parameter_name = sensor["parameter"]["name"].lower()
                    value = sensor["latest_measurement"]["value"]
                    sensor["aqi"] = get_aqi_category(parameter_name, value)
        
        # Get current time for displaying when data was fetched
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return render_template('location.html', location=location_data, fetch_time=current_time)
    
    except requests.RequestException as e:
        return render_template('error.html', message=f"API Error: {str(e)}")
    except Exception as e:
        return render_template('error.html', message=f"Error: {str(e)}")

if __name__ == '__main__':
    # This is used when running locally
    app.run(host='127.0.0.1', port=8080, debug=True)
