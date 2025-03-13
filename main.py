import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

import math

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json",
    "lang": 'RU_ru'
}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym_coodrinates = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ','.join(toponym_coodrinates.split()),
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)

if not response:
    # обработка ошибочной ситуации
    pass

json_response = response.json()
pharmacy_coordinates = json_response['features'][0]['geometry']['coordinates']

address = json_response['features'][0]['properties']['CompanyMetaData']['address']

name = json_response['features'][0]['properties']['CompanyMetaData']['name']

work_hours = json_response['features'][0]['properties']['CompanyMetaData']['Hours']['text']

x1, y1, x2, y2 = *pharmacy_coordinates, *toponym_coodrinates.split()
x2, y2 = float(x2), float(y2)

distance1 = x2 - x1
distance2 = y2 - y1

distance1 *= 111
distance2 = distance2 * 111 * math.cos((x2 + x1 / 2))
distance = (distance1 ** 2 + distance2 ** 2) ** 0.5

if distance >= 1:
    distance = f'{distance // 1} км, {(distance % 1 * 1000) // 1} м'
    
else:
    distance = f'{(distance % 1 * 1000) // 1} м'

print(address, name, work_hours, distance, sep='\n')

apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "pt": f'{",".join([str(i) for i in pharmacy_coordinates])},flag~{",".join(toponym_coodrinates.split())},ya_ru',
    "apikey": apikey,
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

if not response:
    # обработка ошибочной ситуации
    pass

im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()
