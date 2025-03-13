import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

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
    "type": "biz",
    'results': '10'
}

response = requests.get(search_api_server, params=search_params)

if not response:
    # обработка ошибочной ситуации
    pass

json_response = response.json()

pt = []
for i in range(10):
    coord = json_response['features'][i]['geometry']['coordinates']
    
    try:
        a = json_response['features'][i]['properties']['CompanyMetaData']['Hours']
        
        try:
            if json_response['features'][i]['properties']['CompanyMetaData']['Hours']['Availabilities'][0]['TwentyFourHours']:
                color = 'gn'
            
        except Exception:
            color = 'bl'
    
    except Exception:
        color = 'gr'
        
    pt.append(f'{",".join([str(i) for i in coord])},pm2{color}m')

apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "pt": '~'.join(pt),
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
