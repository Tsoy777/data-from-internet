# 3. Рессурс к парсингу : https://5ka.ru/
# Задача:
# Необходимо собрать все данные с раздела товаров по акции и сохранить в json файлы: где имя файла это имя категории товара.
#
# Структура данных в виде:
#
# {
# category_id: str,  - уникальный идентификатор категории
# category_name: str, - человекочитаемое имя категории
# items: list - список товаров пренадлежищий к данной категории
# }
import requests
import time
import json
import codecs

headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.3.320 Yowser/2.5 Safari/537.36'}

# Класс товаров по категориям
class offers_by_category:
    category_id = ""
    category_name = ""
    items = []
    params = {}
    def __init__(self, category_id: str, category_name: str):
        self.category_id = category_id
        self.category_name = category_name
        self.params = {"categories": category_id}
        api_url = 'https://5ka.ru/api/v2/special_offers/'
        self.items = self.get_data(api_url, self.params)
        if len(self.items) > 0:
            self.save_to_json_file()
    def get_response(self, url: str, params: {}):
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    def get_data(self, url: str, params: {}):
        data = []
        while url != None:
            result = self.get_response(url, params=params)
            data.extend(result['results'])
            url = result['next']
            time.sleep(0.5)
        return data
    def save_to_json_file(self):
        data = {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'items': self.items
        }
        with codecs.open('data\\{}.json'.format(self.category_name.replace('*','').replace("\n","").replace('"','')), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, sort_keys=False, indent=4)

def get_response(url: str):
    response = requests.get(url, headers=headers)
    return response.json()

def get_categories(url: str):
    data = []
    result = get_response(url)
    data.extend(result)
    time.sleep(0.5)
    return data

api_url_category = 'https://5ka.ru/api/v2/categories/'
result_category = get_categories(api_url_category)
for category in result_category:
    cur_offers = offers_by_category(category['parent_group_code'],category['parent_group_name'])

print(1)