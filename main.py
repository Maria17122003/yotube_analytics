# Имппортируем необходимое библиотеки
import os
import json
import datetime
import isodate as isodate
from googleapiclient.discovery import build


class Service:
    def get_service(self):
        """
        Возвращает объект
        для работы с API ютуба
        """
        api_key: str = os.getenv('api_key')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class YoutubeApiError(Exception):
    """Класс-исключение для ошибок, связанных с ютубом"""

    def __init__(self, *args):
        self.message = args[0] if args else "Некорректное id видео"

    def __str__(self):
        return self.message


class Channel(Service):
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


class Video(Service):

    def __init__(self, video_id):
        """
        Инициализирует
        атрибуты класса по id видео,
        выдает исключение если
        id неверный
        """
        try:
            self.video = self.get_service().videos().list(part='snippet,statistics', id=video_id).execute()
            if self.video['items']:
                self.video_name = self.video['items'][0]['snippet']['title']
                self.view_count = self.video['items'][0]['statistics']['viewCount']
                self.like_count = self.video['items'][0]['statistics']['likeCount']
            else:
                self.video_name = None
                self.view_count = None
                self.like_count = None
        except YoutubeApiError:
            print('Некорректное id видео')

    def __str__(self):
        return f'{self.video_name}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        """
        Инициализирует
        атрибуты класса по id видео 
        и плейлиста
        """
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist = self.get_service().playlists().list(id=playlist_id,
                                                            part='snippet, contentDetails, status').execute()
        self.playlist_name = self.playlist['items'][0]['snippet']['title']
        self.video_name = self.video['items'][0]['snippet']['title']
        self.view_count = self.video['items'][0]['statistics']['viewCount']
        self.like_count = self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.video_name} ({self.playlist_name})'


class PlayList(Service):
    def __init__(self, playlist_id):
        """
        """
        self.playlist_id = playlist_id
        self.playlist = self.get_service().playlists().list(id=playlist_id,
                                                            part='snippet, contentDetails, status').execute()
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                       part='contentDetails',
                                                                       maxResults=50).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                               id=','.join(self.video_ids)).execute()
        self.playlist_name = self.playlist['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id

    def __repr__(self) -> str:
        return f"('PlayList ({self.playlist_id}))"

    @property
    def total_duration(self):
        """
        Возвращает суммарную
        длительность плейлиста
        """
        total_duration = datetime.timedelta()

        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на
        самое популярное видео из плейлиста
        (по количеству лайков)
        """
        likes = []
        videos = {}

        for video in range(len(self.video_ids)):
            videos[self.video_response['items'][video]['statistics']['likeCount']] = self.video_ids[video]
            likes.append(int(self.video_response['items'][video]['statistics']['likeCount']))
        return f"//youtu.be/{videos[str(max(likes))]}"
