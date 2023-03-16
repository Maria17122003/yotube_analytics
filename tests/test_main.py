import pytest
from main import *


@pytest.fixture()
def channel_1():
    channel_1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    return channel_1


@pytest.fixture()
def channel_2():
    channel_2 = Channel('UC4xZXizv7SCrct1j4IIzMzQ')
    return channel_2


@pytest.fixture()
def file():
    channel = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    file = channel.to_json('file')
    return file


@pytest.fixture()
def video1():
    video1 = Video('9lO06Zxhu88')
    return video1


@pytest.fixture()
def video2():
    video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
    return video2


@pytest.fixture()
def playlist():
    playlist = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
    return playlist


def test_str(channel_1, video1, video2):
    """
    Тест
    __str__
    """
    assert str(channel_1) == 'Youtube-канал: вДудь'
    assert str(video1) == 'Как устроена IT-столица мира / Russian Silicon Valley (English subs)'
    assert str(video2) == 'Пушкин: наше все? (Литература)'


def test_add(channel_1, channel_2):
    """
    Тест
    __add__
    """
    assert channel_1 + channel_2 == 11410000


def test_lt(channel_1, channel_2):
    """
    Тест
    __lt__
    """
    assert channel_1.__lt__(channel_2) is False


def test_gt(channel_1, channel_2):
    """
    Тест
    __gt__
    """
    assert channel_1.__gt__(channel_2) is True


def test_print(capsys):
    """
    Тест
    print_info
    """
    print('Test print')
    captured = capsys.readouterr()
    assert captured.out == 'Test print\n'


def test_to_json():
    """
    Тест
    to_json
    """
    with open("filename.json", encoding="UTF-8") as name_file:
        operations = json.load(name_file)
        for value in operations.values():
            assert value in ["вДудь", "Здесь задают вопросы",
                             "//www.youtube.com/channel/UCMCgOm8GZkHp8zJ6l7_hIuA",
                             "10300000", "165", "1962244295"]


def test_total_duration(playlist):
    """
    Тест
    total_duration
    """
    assert playlist.playlist_name == "Редакция. АнтиТревел"
    assert playlist.url == "https://www.youtube.com/playlist?list=PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb"
    duration = playlist.total_duration
    assert duration == datetime.timedelta(seconds=13261)
    assert duration.total_seconds() == 13261.0


def test_show_best_video(playlist):
    assert playlist.show_best_video() == "//youtu.be/9Bv2zltQKQA"
