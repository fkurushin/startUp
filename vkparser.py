import vk  # https://dev.vk.com
import os
import json
import requests
from tqdm import tqdm
from langdetect import detect

dev_i = '0'
session_j = '1'
num_k = 0

GROUP_ID = '-27685949'  # ID группы или страницы человека(которых парсить) с минусом вначале https://regvk.com/id/
num_posts = 100  # Количество постов для обработки, число кратное 100

data = list()  # Сначала сюда зпишу все json словари
data_k = dict()

# Создание файлов в директории проекта
os.system('mkdir -p photos')
os.system('mkdir -p jsons')

# Захожу в директорию где должны храниться изображения проекта
os.chdir('photos')

for i in tqdm(range(num_posts // 100)):
    # я создал переменную среды со своим access_token, это токен, который можно получить https://vkhost.github.io
    # его нужно обновлять, чтобы скачивать актуальные мемы. А не только те, которые были на момент регистрации токена
    session = vk.Session(os.environ['access_token'])
    api = vk.API(session)
    posts = api.wall.get(owner_id=GROUP_ID, offset=i * 100, count=num_posts, extended=1, v=5.84)
    # posts - это словарь, ключи count, items, next_from, profiles, groups
    # с параметром extended=1 в posts['items'] возварщаестя массив постов, то что надо!

    for post in posts['items']:

        # Отбираем не рекламные посты и содержащие только одно приложение
        # if 'attachments' in posts:
        try:
            if post['marked_as_ads'] == 0 and len(post['attachments']) == 1:

                # Первый индекс равен нулю так как при рассмотрении постов только
                # С одним приложением нет надобности в цикле по приложением, берем 0
                # Индекс 0,1,2,3 в данном случае 3 обозначает качество и размер изображения
                if post['attachments'][0]['type'] == 'photo':

                    url = post['attachments'][0]['photo']['sizes'][3]['url']
                    img_name = 'startup_img_' + dev_i + '_' + session_j + '_' + str(num_k) + '.jpg'
                    r = requests.get(url, allow_redirects=True)
                    open(img_name, 'wb').write(r.content)

                    if post['text'] == '':
                        data_k = {'name': img_name,
                                  'text': 'None',
                                  'lang': 'None'
                                  }
                    else:
                        data_k = {'name': img_name,
                                  'text': post['text'],
                                  'lang': detect(post['text'])
                                  }

                    data.append(data_k)
                    num_k += 1
                else:
                    continue

        except KeyError:
            pass

# Переход в другую директорию
os.chdir('..')
os.chdir('jsons')

# Создание json файлов
for idx, data_i in enumerate(data):
    json_name = 'startup_' + dev_i + '_' + session_j + '_' + str(idx) + '.json'
    with open(json_name, "w") as file:
        json.dump(data_i, file, ensure_ascii=False)
