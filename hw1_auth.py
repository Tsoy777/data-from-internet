# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.
import requests
import json
import codecs
from getpass import getpass

headers = {
    'User-agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.3.320 Yowser/2.5 Safari/537.36',
    'Accept':'application/vnd.github.nebula-preview+json',
    'Authorization' : 'token OAUTH-TOKEN'
}

username = 'Tsoy777'
password = getpass()

url = 'https://api.github.com/user'
response = requests.get(url, auth=(username, password), headers=headers)

with codecs.open('auth_response\\auth_response.json', 'w', encoding='utf-8') as f:
     json.dump(response.json(), f, indent=4)

print(1)
