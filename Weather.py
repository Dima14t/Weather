import requests  # Импортирует библиотеку requests для отправки HTTP-запросов и получения данных с веб-сайтов.
from bs4 import BeautifulSoup  # Импортирует библиотеку BeautifulSoup для парсинга HTML-кода.
import json  # Импортирует библиотеку json для работы с данными в формате JSON.

def get_html(url: str):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'}
    response = requests.get(url, headers=headers)
    return response.text

def get_weather(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    dates = soup.find_all('div', class_='dates short-d')  # Получаем все даты

    weather = {}

    table = soup.find('table', class_='weather-today short')
    rows = table.find_all('tr')

    for i, row in enumerate(rows):
        if i < len(dates):  # Проверяем, чтобы не выйти за пределы списка дат
            date = dates[i].text.strip()  # Получаем дату
            weather[date] = {}  # Инициализируем словарь для этой даты

            # Извлекаем данные для каждого временного периода
            for period in ['Ночь', 'Утро', 'День', 'Вечер']:
                weather_day = row.find('td', class_='weather-day').text.strip()
                temperature = row.find('td', class_='weather-temperature').text.strip()
                conditions = row.find('td', class_='weather-temperature').find('div')['title']
                feeling = row.find('td', class_='weather-feeling').text.strip()
                probability = row.find('td', class_='weather-probability').text.strip()
                pressure = row.find('td', class_='weather-pressure').text.strip()
                wind_direction = row.find('td', class_='weather-wind').find_all('span')[0]['title']
                wind_speed = row.find('td', class_='weather-wind').find_all('span')[1].text.strip()

                weather[date][period] = {
                    'temperature': temperature,
                    'conditions': conditions,
                    'feeling': feeling,
                    'probability': probability,
                    'pressure': pressure,
                    'wind_direction': wind_direction,
                    'wind_speed': wind_speed
                }
    return weather

def write_weather_json(weather: dict):
    with open('weather.json', 'w', encoding='utf-8') as file:
        json.dump(weather, file, indent=2, ensure_ascii=False)

URL = "https://world-weather.ru/pogoda/russia/saint_petersburg/7days/"
html = get_html(url=URL)
weather = get_weather(html)
write_weather_json(weather)
