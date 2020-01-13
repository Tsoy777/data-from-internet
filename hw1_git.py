# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
import requests
import json
import codecs

headers = {
    'User-agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.3.320 Yowser/2.5 Safari/537.36',
    'Accept':'application/vnd.github.nebula-preview+json'
}

def get_response(url: str):
    response = requests.get(url, headers=headers)
    return response.json()

url_repo = 'https://api.github.com/users/Tsoy777/repos'
result_repo = get_response(url_repo)

with codecs.open('repo\\repositories.json', 'w', encoding='utf-8') as f:
    json.dump(result_repo, f, indent=4)

print(1)