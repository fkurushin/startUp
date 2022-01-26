import vk  # https://dev.vk.com
import os
import requests
from tqdm import tqdm

GROUP_ID = '-166884737'  # ID группы или страницы человека(которых парсить) с минусом вначале https://regvk.com/id/
num_posts = 2  # Количество постов

os.system('mkdir photos')

# я создал переменную среды со своим access_token, это токен, который можно получить https://vkhost.github.io
# его нужно обновлять, чтобы скачивать актуальные мемы. А не только те, которые были на момент регистрации токена
session = vk.Session(os.environ['access_token'])
api = vk.API(session)
posts = api.wall.get(owner_id=GROUP_ID, count=num_posts, extended=1, v=5.84)  # Это словарь, ключи count, items, next_from


# это было при параметре extended=0
# for item in tqdm(posts['items']):
#     # item, это тоже словарь, который содержит в себе много полей, в том числе, что было в посте, комментарии лайки,
#     # ссылки на фото и еще много интересной информации, сортировать по времени их надо, но не понятно пока, как илентифицировать фото из одного поста, потому что фотки лежат все в одном месте
#     for attachment in item['attachments']:
#         # Индекс 0,1,2,3 в данном случае 3 обозначает качество и размер изображения
#         url = attachment['photo']['sizes'][3]['url']
#         name = 'photos/' + os.path.basename(url)[:15]
#         r = requests.get(url, allow_redirects=True)
#         open(name, 'wb').write(r.content)

# с параметром extended=1 в posts['items'] возварщаестя массив постов, то что надо!
for post in posts['items']:
    for attachment in post['attachments']:
        url = attachment['photo']['sizes'][3]['url']
        name = 'photos/' + str(post['id']) + os.path.basename(url)[:15]
        r = requests.get(url, allow_redirects=True)
        open(name, 'wb').write(r.content)
