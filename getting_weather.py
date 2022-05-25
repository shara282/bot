import requests
from config import API_LINK_WEATHER, API_LINK_AIR_POLLUTION, API_LINK_GEO
import datetime

smile_code_weather = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U0001F327",
    "Drizzle": "Мелкий дождь \U0001F4A7",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}

smile_code_air_pollution = {
    1: "1 - хорошо \U0001F603",
    2: "2 - удовлетворительно \U0001F60A",
    3: "3  - умеренно \U0001F610",
    4: "4 - плохо \U0001F61F",
    5: "5 - очень плохо \U0001F616",

}


def get_weather(text, i, WEATHER_TOKEN):  # 1 - По городу, 2 - По координатам
    if i == 1:
        request = requests.get(API_LINK_WEATHER + f"q={text}&appid={WEATHER_TOKEN}&units=metric")
    elif i == 2:
        request = requests.get(API_LINK_WEATHER + f"lat={text[0]}&lon={text[1]}&appid={WEATHER_TOKEN}&units=metric")
    data = request.json()
    city_name = data["name"]
    lon = data["coord"]["lon"]
    lat = data["coord"]["lat"]
    weather_description = data["weather"][0]["main"]
    if weather_description in smile_code_weather:
        weather_description = smile_code_weather[weather_description]
    else:
        weather_description = "Группа погодных параметров не определена"
    temp = data["main"]["temp"]
    temp_feels = temp = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    visibility = data["visibility"]
    wind_speed = data["wind"]["speed"]
    wind_gust = data["wind"]["gust"]
    clouds = data["clouds"]["all"]
    sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    day_length = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
        data["sys"]["sunrise"])
    a = {'city_name': city_name, 'lon': lon, 'lat': lat, 'weather_description': weather_description,
         'temp': temp, 'temp_feels': temp_feels, 'humidity': humidity, 'pressure': pressure,
         'visibility': visibility, 'wind_speed': wind_speed, 'wind_gust': wind_gust, 'clouds': clouds,
         'sunrise_time': sunrise_time, 'sunset_time': sunset_time, 'day_length': day_length}
    return a


def get_air_pollution(text, i, WEATHER_TOKEN):  # 1 - По городу, 2 - По координатам
    if i == 1:
        request1 = requests.get(API_LINK_GEO + f"q={text}&limit=1&appid={WEATHER_TOKEN}")
        data1 = request1.json()
        city_name = data1[0]["name"]
        lon_1 = data1[0]["lon"]
        lat_1 = data1[0]["lat"]
        request = requests.get(API_LINK_AIR_POLLUTION + f"lat={lat_1}&lon={lon_1}&appid={WEATHER_TOKEN}")
    elif i == 2:
        request = requests.get(API_LINK_AIR_POLLUTION + f"lat={text[0]}&lon={text[1]}&appid={WEATHER_TOKEN}")
    data = request.json()
    lon = data["coord"]["lon"]
    lat = data["coord"]["lat"]
    aqi = data["list"][0]["main"]["aqi"]
    if aqi in smile_code_air_pollution:
        aqi = smile_code_air_pollution[aqi]
    co = data["list"][0]["components"]["co"]
    no = data["list"][0]["components"]["no"]
    no2 = data["list"][0]["components"]["no2"]
    o3 = data["list"][0]["components"]["o3"]
    so2 = data["list"][0]["components"]["so2"]
    pm2_5 = data["list"][0]["components"]["pm2_5"]
    pm10 = data["list"][0]["components"]["pm10"]
    nh3 = data["list"][0]["components"]["nh3"]
    if i == 1:
        a = {'city_name': city_name, 'lon': lon, 'lat': lat, 'aqi': aqi, 'co': co, 'no': no, 'no2': no2,
             'o3': o3, 'so2': so2, 'pm2_5': pm2_5, 'pm10': pm10, 'nh3': nh3}
        return a
    elif i == 2:
        a = {'lon': lon, 'lat': lat, 'aqi': aqi, 'co': co, 'no': no, 'no2': no2,
             'o3': o3, 'so2': so2, 'pm2_5': pm2_5, 'pm10': pm10, 'nh3': nh3}
        return a
