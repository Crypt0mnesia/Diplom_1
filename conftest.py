import pytest
from unittest.mock import Mock


@pytest.fixture
def bun():
    """Базовая фикстура для булочки"""
    mock = Mock()
    mock.get_name.return_value = "Тестовая булочка"
    mock.get_price.return_value = 100
    return mock


@pytest.fixture
def ingredient_sauce():
    """Фикстура для соуса"""
    mock = Mock()
    mock.get_type.return_value = "SAUCE"
    mock.get_name.return_value = "Тестовый соус"
    mock.get_price.return_value = 50
    return mock


@pytest.fixture
def ingredient_filling():
    """Фикстура для начинки"""
    mock = Mock()
    mock.get_type.return_value = "FILLING"
    mock.get_name.return_value = "Тестовая начинка"
    mock.get_price.return_value = 75
    return mock