# Имппортируем необходимое библиотеки
import os
import json
from googleapiclient.discovery import build


class Channel:
    def __init__(self, channel_id):
        """
        Инициализирует
        айдишник (id) конкретного
        ютуб-канала
        """
        self.channel_id = channel_id

    def print_info(self):
        """
        Выводит в консоль
        информацию о канале
        """
        api_key: str = os.getenv('api_key')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return json.dumps(channel, indent=2, ensure_ascii=False)
