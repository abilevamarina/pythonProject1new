import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import json

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import load_json_data, get_amount_in_rubles


class TestLoadJsonData(unittest.TestCase):
    """Тесты для функции load_json_data"""


def setup():
    """Настройка тестовых данных"""
    valid_json_data = [
        {"id": 1, "name": "Transaction 1"},
        {"id": 2, "name": "Transaction 2"}
    ]

    invalid_json_data = {"id": 1, "name": "Not a list"}


    def test_load_json_data_success():
        """Тест успешной загрузки JSON файла"""
        # Создаем мок для open и json.load
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            with patch("json.load") as mock_json_load:
                mock_json_load.return_value = "valid_json_data"

                # Вызываем функцию
                result = load_json_data("test.json")
                # Проверяем результат
                assert(result, "valid_json_data")
                mock_file.assert_called_once_with("test.json", "r", encoding="utf-8")

    def test_load_json_data_file_not_found():
        """Тест случая, когда файл не существует"""
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = False

            result = load_json_data("nonexistent.json")
            assert(result, [])

    def test_load_json_data_empty_file():
        """Тест случая, когда файл пустой"""
        with patch("os.path.exists") as mock_exists:
            with patch("os.path.getsize") as mock_getsize:
                mock_exists.return_value = True
                mock_getsize.return_value = 0

                result = load_json_data('empty.json')
                assert(result, [])

    def test_load_json_data_invalid_json():
        """Тест случая с невалидным JSON"""
        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            with patch('json.load') as mock_json_load:
                mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)

                result = load_json_data('invalid.json')
                assert(result, [])

    def test_load_json_data_io_error():
        """Тест случая с ошибкой ввода-вывода"""
        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            with patch('json.load') as mock_json_load:
                mock_json_load.side_effect = IOError("File read error")

                result = load_json_data('error.json')
                assert(result, [])

    def test_load_json_data_not_a_list():
        """Тест случая, когда JSON не является списком"""
        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            with patch('json.load') as mock_json_load:
                mock_json_load.return_value = invalid_json_data

                result = load_json_data('not_list.json')
                assert(result, [])


class TestGetAmountInRubles(unittest.TestCase):
    """Тесты для функции get_amount_in_rubles из utils"""


def setUp():
    """Настройка тестовых данных"""
    test_transaction_rub = {
        "id": 1,
        "operationAmount": {
            "amount": "100.50",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        }
    }

    @patch('utils.get_transaction_amount_in_rubles')
    def test_get_amount_in_rubles(mock_external_func):
        """Тест функции-обертки из utils"""
        # Мокаем функцию из external_api
        mock_external_func.return_value = 100.50

        # Вызываем функцию
        result = get_amount_in_rubles("test_transaction_rub")

        # Проверяем результат
        assert(result, 100.50)

        # Проверяем вызов внешней функции
        mock_external_func.assert_called_once_with("test_transaction_rub")
