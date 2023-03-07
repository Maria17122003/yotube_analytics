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


def test_str(channel_1):
    """
    Тест
    __str__
    """
    assert str(channel_1) == 'Youtube-канал: вДудь'


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
    print('Test print')
    captured = capsys.readouterr()
    assert captured.out == 'Test print\n'


def test_to_json():
    with open("filename.json", encoding="UTF-8") as name_file:
        operations = json.load(name_file)
        for value in operations.values():
            assert value in ["вДудь", "Здесь задают вопросы",
                             "//www.youtube.com/channel/UCMCgOm8GZkHp8zJ6l7_hIuA",
                             "10300000", "165", "1962244295"]
