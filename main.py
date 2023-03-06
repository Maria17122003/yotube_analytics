# Имппортируем необходимое библиотеки
import os
import json
from googleapiclient.discovery import build


class Channel:
    def __init__(self, channel_id):
        """
        Инициализирует
        атрибуты класса по id канала
        """
        self.__channel_id = channel_id
        info = self.print_info()
        self.item = json.loads(info)
        self.name_channel = self.item['items'][0]['snippet']['title']
        self.description = self.item['items'][0]['snippet']['description']
        self.channel_link = "//www.youtube.com/channel/" + self.item['items'][0]['id']
        self.subscribers = self.item['items'][0]['statistics']['subscriberCount']
        self.video_count = self.item['items'][0]['statistics']['videoCount']
        self.total_views = self.item['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'Youtube-канал: {self.name_channel}'

    def __add__(self, other):
        """
        Складывает количество
        подписчиков
        """
        return int(self.subscribers) + int(other.subscribers)

    def __lt__(self, other):
        """
        Сравнивает количество
        подписчиков
        """
        if int(self.subscribers) < int(other.subscribers):
            return True
        return False

    def __gt__(self, other):
        """
        Сравнивает количество
        подписчиков
        """
        if int(self.subscribers) > int(other.subscribers):
            return True
        return False

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    def get_service(self):
        """
        Возвращает объект
        для работы с API ютуба
        """
        api_key: str = os.getenv('api_key')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def print_info(self):
        """
        Выводит в консоль
        информацию о канале
        """
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return json.dumps(channel, indent=2, ensure_ascii=False)

    def to_json(self, name_file):
        """
        Сохраняет информацию
        по каналу,
        хранящуюся в атрибутах
        экземпляра класса
        """
        data = {
            "title": self.name_channel,
            "description": self.description,
            "url": self.channel_link,
            "subscriberCount": self.subscribers,
            "videoCount": self.video_count,
            "viewCount": self.total_views
        }
        with open("filename.json", "w", encoding="UTF-8") as name_file:
            json.dump(data, name_file, indent=2, ensure_ascii=False)
