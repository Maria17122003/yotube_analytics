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
