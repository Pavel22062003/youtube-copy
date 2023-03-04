import os
import json
import isodate
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


    def __str__(self):
        """Возвращает название канала"""
        return f'Youtube-канал: {self.name}'
    def __add__(self, other):
        return self.amount_subscribers + other.amount_subscribers

    def __gt__(self, other):
        """Сравнивает кол-во подписчиков и возвращает True или False"""
        if self.amount_subscribers > other.amount_subscribers:
            return True
        return False

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

class Video:

    def __init__(self,id:str):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.id = id
        video_response = youtube.videos().list(part='snippet,statistics',
                                               id=self.id
                                               ).execute()

        self.title: str = video_response['items'][0]['snippet']['title']
        self.view_count: int = int(video_response['items'][0]['statistics']['viewCount'])
        self.like_count: int = int(video_response['items'][0]['statistics']['likeCount'])
        self.comment_count: int = int(video_response['items'][0]['statistics']['commentCount'])

    def __str__(self):
        """возвращает название видео"""
        return self.title

class PLVideo(Video):
    def __init__(self, video_id:str, playlist_id:str):
        super().__init__(video_id)
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist_id = playlist_id

        playlist = youtube.playlists().list(id=playlist_id, part='snippet').execute()
        self.playlist_name = playlist['items'][0]['snippet']['title']

    def __str__(self):
        """возвращает название видео и название плэйлиста"""
        return f'{super().__str__()} ({self.playlist_name})'

class PlayList(Video):
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, playlist_id):

        playlist_id = 'PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb'  # Редакция. АнтиТревел
        playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        self.__playlist_id = playlist_id

        playlist = self.youtube.playlists().list(id=playlist_id, part='snippet').execute()
        self.playlist_name = playlist['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'
        self.__video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
    @property
    def total_duratuion(self):
        """Показывают общую продолжительность плэй листа"""
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.__video_ids)
                                               ).execute()
        # printj(video_response)
        duration_amount = 0
        for video in video_response['items']:

            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            if duration_amount == 0:
                duration_amount = duration
            else:
                 duration_amount += duration
        return duration_amount

    def show_best_video(self):
       """Выводит самое популярное видео из плэй листа на основе лайков"""
       counter = 0
       id = ''
       for i in self.__video_ids:
         super().__init__(i)
         if self.like_count > counter:
             counter = self.like_count
             id = self.id
       return f'https://youtu.be/{id}'



c = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
print(c.total_duratuion)
print(type(c.total_duratuion))


        



