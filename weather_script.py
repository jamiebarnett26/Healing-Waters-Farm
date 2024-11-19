import requests 

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "f7f03cd502fc96f80005c17688567b60"
# To get the city id:
# 1) go to openweathermap.org
# 2) Search the city, and at the end of the URL is the city ID
CITY_ID = "5102922"
url = BASE_URL + "appid=" + API_KEY + "&id=" + CITY_ID

response = requests.get(url).json()

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

# return tuple(celsius, fahrenheit)
def get_weather():
    temp_kelvin = response['main']['temp']
    return kelvin_to_celsius_fahrenheit(temp_kelvin)   

# return tuple(celsius, fahrenheit)
def get_feels_like_weather():
    feels_like_kelvin = response['main']['feels_like']
    return kelvin_to_celsius_fahrenheit(feels_like_kelvin)

def get_humidity():
    return response['main']['humidity']

# Returns the description of the weather: e.g., clear sky
def get_description():
    return response['weather'][0]['description']

def get_city():
    return response['name']
