import requests 

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "f7f03cd502fc96f80005c17688567b60"
# To get the city id:
# 1) go to openweathermap.org
# 2) Search the city, and at the end of the URL is the city ID
CITY_ID = "5102922"
url = BASE_URL + "appid=" + API_KEY + "&id=" + CITY_ID

response = requests.get(url).json()

def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return round(celsius)

def kelvin_to_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return round(fahrenheit)
    
def get_fahrenheit():
    temp_kelvin = response['main']['temp']
    return kelvin_to_fahrenheit(temp_kelvin)  

def get_celsius():
    temp_kelvin = response['main']['temp']
    return kelvin_to_celsius(temp_kelvin)  


def get_humidity():
    return response['main']['humidity']

# Returns the description of the weather: e.g., clear sky
def get_description():
    return response['weather'][0]['description']

def get_city():
    return response['name']

def get_wind_speed():
    wind_speed_mps = response['wind']['speed']
    wind_speed_mph = wind_speed_mps * 2.23694
    return round(wind_speed_mph, 2)

def get_kelvin():
    return response['main']['temp']
