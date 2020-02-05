import vk_api
from pymongo import MongoClient

mongo_client = MongoClient()
database = mongo_client['vk']
collection = database['vk_chain_friends']
all_users = []

#Авторизация вк
def vk_auth():
    phone_number = str(input("Введите номер телефона в формате +7**********:  "))
    vk_session = vk_api.VkApi(phone_number)
    vk_session.auth()
    vk = vk_session.get_api()
    return vk

#Класс польлзователь. С помощью него можно будет легко находить "родителей" пользователя
class user:
    user_id = 0
    parent_id = 0
    level = 0
    def __init__(self, user_id: int, parent_id: int, level: int):
        self.user_id = user_id
        self.parent_id = parent_id
        self.level = level
    pass

#Функция по нахождению уникальных друзей у можества пользователей
def friends_by_users2(vk, start_ids: set, all_ids: set, level: int, another_set: set):
    friends = set()
    for start_id in start_ids:
        try:
            cur_friends = set(vk.friends.get(user_id=start_id)['items']).difference(all_ids)
            fill_user_data(cur_friends, start_id, level = level)
            all_ids.update(cur_friends)
            friends.update(cur_friends)
            if len(all_ids.intersection(another_set)):
                return [friends, all_ids]
        except:
            pass
    return [friends, all_ids]

#Функция по сближению двух пользователей: сначала находим друзей одного из пользователей, затем у другого,
#не забывая проверять пересечение этих двух множеств
def user_converge(start_id: int, target_id: int, vk):
    all_ids_r = set()
    all_ids_l = set()
    start_ids = set()
    target_ids = set()

    status = True

    start_ids.add(start_id)
    target_ids.add(target_id)
    all_ids_r.add(start_id)
    all_ids_l.add(target_id)
    fill_user_data(start_ids,0,0)
    fill_user_data(target_ids,0,0)

    result = friends_by_users2(vk, start_ids, all_ids_r, 0, all_ids_l)
    all_ids_r.update(result[1])
    start_ids.clear()
    start_ids.update(result[0])
    print("right", len(start_ids))
    while len(all_ids_r.intersection(all_ids_l)) == 0:
        if status:
            result = friends_by_users2(vk, target_ids, all_ids_l, 0, all_ids_r)
            all_ids_l.update(result[1])
            target_ids.clear()
            target_ids.update(result[0])
            print("left", len(target_ids))
            status = False
        else:
            result = friends_by_users2(vk, start_ids, all_ids_r, 0, all_ids_l)
            all_ids_r.update(result[1])
            start_ids.clear()
            start_ids.update(result[0])
            print("right ", len(start_ids))
            status = True
    return all_ids_r.intersection(all_ids_l)

#Заполнение списка пользователей
def fill_user_data(ids: set, parent_id: int, level: int):
    for id in ids:
        all_users.append(user(id, parent_id, level))

#Нахождение цепочки рукопожатий
def friend_chain2(start_id:int, target_id: int, inter_set: set, vk):

    chain = []
    i = 0
    first_time = True

    for m in inter_set:
        elem = m
    while elem != target_id and elem != start_id:
        chain.append([s for s in all_users if s.user_id == elem][0])
        elem = chain[i].parent_id
        i += 1
    chain.append([s for s in all_users if s.user_id == elem][0])
    isTarget = (True if elem == target_id else False)
    chain.reverse()
    i += 1

    for m in inter_set:
        elem = m
    while elem != target_id and elem != start_id:
        if first_time:
            elem = [s for s in all_users if s.user_id == elem][1].parent_id
            first_time = False
        else:
            chain.append([s for s in all_users if s.user_id == elem][0])
            elem = chain[i].parent_id
            i += 1
    chain.append([s for s in all_users if s.user_id == (start_id if isTarget else target_id)][0])
    return chain

# Функция определения id пользователя по адресу его страницы
def get_id(url: str, vk):
    q = url.split('/')[-1].split('id')[-1]
    try:
        q = int(q)
        user_id = q
        return user_id
    except:
        q = url.split('/')[-1]
        user_id = vk.users.search(q = q)['items'][0]['id']
        return user_id

if __name__ == '__main__':
    vk = vk_auth()
    user_id1 = get_id('https://vk.com/id5383224',vk)
    user_id2 = get_id('https://vk.com/annasesl',vk)
    inter_set = user_converge(user_id1,user_id2,vk)
    chain = friend_chain2(user_id1, user_id2, inter_set, vk)

    for elem in chain:
        collection.insert_one(vk.users.get(user_id=elem.user_id)[0])
        print(vk.users.get(user_id=elem.user_id))
    print(1)