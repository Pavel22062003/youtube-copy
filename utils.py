import os
import json

from googleapiclient.discovery import build


class Chanel:
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id: str):
        self.__id = id
        self.youtube = Chanel.youtube
        # api_key: str = os.getenv('API_KEY')
        # self.youtube = build('youtube', 'v3', developerKey=api_key)
        channel = self.youtube.channels().list(id=self.__id, part='snippet,statistics').execute()
        a = json.dumps(channel, indent=2, ensure_ascii=False)
        self.info = json.loads(a)
        self.name = self.info['items'][0]['snippet']['title']  # имя канала

        self.description = self.info['items'][0]['snippet']['description']  # описание канала
        self.link = 'https://www.youtube.com/channel/' + self.info['items'][0]['id']  # ссылка на канал
        self.amount_subscribers = int(self.info['items'][0]["statistics"]["subscriberCount"])  # кол-во подписчиков
        self.video_amount = int(self.info['items'][0]["statistics"]["videoCount"])  # кол-во видео
        self.amount_views = self.info['items'][0]["statistics"]["viewCount"]  # кол-во просмотров




    @property
    def id(self):
        return self.__id

    """Позволяет получить id канала, но не изменить его"""

    def print_info(self):
        """Выодит всю информацию о канале"""
        return self.info

    def to_json(self, file_name: str):
        """Записывает атрибуты экземпляра класса в json файл"""
        data = {'name': self.info['items'][0]['snippet']['title'],
                'description': self.info['items'][0]['snippet']['description'],
                'link': 'https://www.youtube.com/channel/' + self.info['items'][0]['id'],
                'amount_subscribers': self.info['items'][0]["statistics"]["subscriberCount"],
                'video_amount': self.info['items'][0]["statistics"]["videoCount"],
                'amount_views': self.info['items'][0]["statistics"]["viewCount"]
                }
        with open(file_name, "w", encoding='UTF-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @classmethod
    def get_service(cls):
        """Выводит API объект """
        return cls.youtube

chn1 = Chanel('UC6EBllXkH3haWCoGpdgWMHA')
print(chn1.id)
chn1.id = '123'