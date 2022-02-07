import vk  # https://dev.vk.com
import os
import requests
from tqdm import tqdm

GROUP_ID = '-27685949'  # ID группы или страницы человека(которых парсить) с минусом вначале https://regvk.com/id/
num_posts = 1000  # Количество постов, число кратное 100

os.system('mkdir photos')
fo = open('log.txt', 'a')  # Возможно нужно поменять мод

for i in tqdm(range(num_posts // 100)):
    # я создал переменную среды со своим access_token, это токен, который можно получить https://vkhost.github.io
    # его нужно обновлять, чтобы скачивать актуальные мемы. А не только те, которые были на момент регистрации токена
    session = vk.Session(os.environ['access_token'])
    api = vk.API(session)
    posts = api.wall.get(owner_id=GROUP_ID, offset=i * 100, count=num_posts, extended=1, v=5.84)
    # Это словарь, ключи count, items, next_from, profiles, groups
    # с параметром extended=1 в posts['items'] возварщаестя массив постов, то что надо!

    for post in posts['items']:
        # Отбираем не рекламные посты и содержащие только одно приложение
        # if 'attachments' in posts:
        try:
            if post['marked_as_ads'] == 0 and len(post['attachments']) == 1:

                # Первый индекс  равен нулю так как при рассмотрении постов только
                # С одним приложением нет надобности в цикле по приложением, берем 0
                # Индекс 0,1,2,3 в данном случае 3 обозначает качество и размер изображения
                if post['attachments'][0]['type'] == 'photo':
                    url = post['attachments'][0]['photo']['sizes'][3]['url']
                    name = 'photos/' + str(post['id']) + os.path.basename(url)[:15]
                    r = requests.get(url, allow_redirects=True)
                    open(name, 'wb').write(r.content)

                    # Запись в файл название фотографии и текста поста
                    # Название изображения
                    fo.write(name)
                    fo.write('\t')
                    # Текста поста
                    if post['text'] == '' and post['text'] == ' ' and post['text'] == '  ':
                        fo.write('None')
                    else:
                        if '\n' in post['text']:
                            fo.write(post['text'].replace('\n', '\t'))
                    fo.write('\n')
                else:
                    continue
        except KeyError:
            pass
fo.close()
