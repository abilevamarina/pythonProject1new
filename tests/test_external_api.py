import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from decimal import Decimal

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.external_api import get_exchange_rate, convert_to_rubles, get_transaction_amount_in_rubles
from src.external_api import  RUB_CURRENCY, USD_CURRENCY, EUR_CURRENCY



class TestExternalAPI(unittest.TestCase):
    """Тесты для функций работы с внешним API"""

def setUp():
    """Настройка тестовых данных"""
    test_transaction_rub = {
        "id": 1,
        "operationAmount": {
            "amount": "100.50",
            "currency": {
                "name": "руб.",
                "code": RUB_CURRENCY
            }
        }
    }

    test_transaction_eur = {
        "id": 3,
        "operationAmount": {
            "amount": "30.25",
            "currency": {
                "name": "евро",
                "code": EUR_CURRENCY
            }
        }
    }

    invalid_transaction_no_amount = {
        "id": 4,
        "operationAmount": {
            "currency": {
                "name": "руб.",
                "code": RUB_CURRENCY
            }
        }
    }
    invalid_transaction_no_currency = {
        "id": 5,
        "operationAmount": {
            "amount": "100.00"
        }
    }

@patch('external_api.os.getenv')
@patch('external_api.requests.get')
def test_get_exchange_rate_success(mock_requests_get, mock_getenv):
    """Тест успешного получения курса валют"""
    # Мокаем переменную окружения
    mock_getenv.return_value = "test_api_key"

    # Мокаем ответ API
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "rates": {
            RUB_CURRENCY: 75.50
        },
        "base": USD_CURRENCY,
        "date": "2023-12-01"
    }
    mock_requests_get.return_value = mock_response

    # Вызываем функцию
    rate = get_exchange_rate(USD_CURRENCY, RUB_CURRENCY)

    # Проверяем результат
    assert(rate, 75.50)

    # Проверяем, что запрос был выполнен с правильными параметрами
    mock_requests_get.assert_called_once()
    call_args = mock_requests_get.call_args
    assert(call_args[0][0], "https://apilayer.com/exchangerates_data-api")
    assert(call_args[1]['headers']['apikey'], 'test_api_key')
    assert(call_args[1]['params']['base'], USD_CURRENCY)
    assert(call_args[1]['params']['symbols'], RUB_CURRENCY)

@patch('external_api.os.getenv')
def test_get_exchange_rate_no_api_key(mock_getenv):
    """Тест случая, когда API ключ не установлен"""
    # Мокаем переменную окружения - ключ отсутствует
    mock_getenv.return_value = None

    # Вызываем функцию
    rate = get_exchange_rate(USD_CURRENCY, RUB_CURRENCY)

    # Проверяем результат
    assert(rate, 0.0)

@patch('external_api.os.getenv')
@patch('external_api.requests.get')
def test_get_exchange_rate_request_exception(mock_requests_get, mock_getenv):
    """Тест обработки исключения при запросе к API"""
    # Мокаем переменную окружения
    mock_getenv.return_value = "test_api_key"

    # Мокаем исключение при запросе
    mock_requests_get.side_effect = Exception("Connection error")

    # Вызываем функцию
    rate = get_exchange_rate(USD_CURRENCY, RUB_CURRENCY)

    # Проверяем результат
    assert(rate, 0.0)

@patch('external_api.os.getenv')
@patch('external_api.requests.get')
def test_get_exchange_rate_invalid_response(mock_requests_get, mock_getenv):
    """Тест обработки невалидного ответа API"""
    # Мокаем переменную окружения
    mock_getenv.return_value = "test_api_key"

    # Мокаем ответ API без нужных данных
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "error": "Invalid base currency"
    }
    mock_requests_get.return_value = mock_response

    # Вызываем функцию
    rate = get_exchange_rate(USD_CURRENCY, RUB_CURRENCY)

    # Проверяем результат
    assert(rate, 0.0)

@patch('external_api.get_exchange_rate')
def test_convert_to_rubles_rub(mock_get_exchange_rate):
    """Тест конвертации рублей в рубли (без конвертации)"""
    # Вызываем функцию
    result = convert_to_rubles("100.50", RUB_CURRENCY)

    # Проверяем результат
    assert(result, 100.50)

    # Проверяем, что функция get_exchange_rate не вызывалась
    mock_get_exchange_rate.assert_not_called()

@patch('external_api.get_exchange_rate')
def test_convert_to_rubles_usd_success(mock_get_exchange_rate):
    """Тест успешной конвертации USD в рубли"""
    # Мокаем курс обмена
    mock_get_exchange_rate.return_value = 75.50

    # Вызываем функцию
    result = convert_to_rubles("50.00", USD_CURRENCY)

    # Проверяем результат (50.00 * 75.50 = 3775.00)
    assert(result, 3775.00)

    # Проверяем вызов функции get_exchange_rate
    mock_get_exchange_rate.assert_called_once_with(USD_CURRENCY, RUB_CURRENCY)

@patch('external_api.get_exchange_rate')
def test_convert_to_rubles_eur_success(mock_get_exchange_rate):
    """Тест успешной конвертации EUR в рубли"""
    # Мокаем курс обмена
    mock_get_exchange_rate.return_value = 85.25

    # Вызываем функцию
    result = convert_to_rubles("30.25", EUR_CURRENCY)

    # Проверяем результат (30.25 * 85.25 = 2578.8125 -> округляется до 2578.81)
    assert(result, 2578.81)

@patch('external_api.get_exchange_rate')
def test_convert_to_rubles_invalid_amount(mock_get_exchange_rate):
    """Тест конвертации с невалидной суммой"""
    # Вызываем функцию с невалидной строкой
    result = convert_to_rubles("not_a_number", USD_CURRENCY)

    # Проверяем результат
    assert(result, 0.0)

@patch('external_api.get_exchange_rate')
def test_convert_to_rubles_zero_exchange_rate(mock_get_exchange_rate):
    """Тест конвертации с нулевым курсом обмена"""
    # Мокаем нулевой курс обмена
    mock_get_exchange_rate.return_value = 0.0

    # Вызываем функцию
    result = convert_to_rubles("100.00", USD_CURRENCY)

    # Проверяем результат
    assert(result, 0.0)

@patch('external_api.get_exchange_rate')
def test_get_transaction_amount_in_rubles_rub():
    """Тест получения суммы в рублях для транзакции в рублях"""
    # Вызываем функцию
    result = get_transaction_amount_in_rubles("test_transaction_rub")

    # Проверяем результат
    assert(result, 100.50)

@patch('external_api.convert_to_rubles')
def test_get_transaction_amount_in_rubles_usd(mock_convert_to_rubles):
    """Тест получения суммы в рублях для транзакции в долларах"""
    # Мокаем результат конвертации
    mock_convert_to_rubles.return_value = 3775.00

    # Вызываем функцию
    result = get_transaction_amount_in_rubles("test_transaction_usd")

    # Проверяем результат
    assert(result, 3775.00)

    # Проверяем вызов функции convert_to_rubles с правильными параметрами
    mock_convert_to_rubles.assert_called_once_with("50.00", USD_CURRENCY)


@patch('external_api.convert_to_rubles')
def test_get_transaction_amount_in_rubles_eur(mock_convert_to_rubles):
    """Тест получения суммы в рублях для транзакции в евро"""
    # Мокаем результат конвертации
    mock_convert_to_rubles.return_value = 2578.81

    # Вызываем функцию
    result = get_transaction_amount_in_rubles("test_transaction_eur")

    # Проверяем результат
    assert(result, 2578.81)

    # Проверяем вызов функции convert_to_rubles с правильными параметрами
    mock_convert_to_rubles.assert_called_once_with("30.25", EUR_CURRENCY)


def test_get_transaction_amount_in_rubles_no_operation_amount():
    """Тест для транзакции без operationAmount"""
    transaction = {"id": 6}
    result = get_transaction_amount_in_rubles(transaction)
    assert(result, 0.0)


def test_get_transaction_amount_in_rubles_empty_operation_amount():
    """Тест для транзакции с пустым operationAmount"""
    transaction = {"id": 7, "operationAmount": {}}
    result = get_transaction_amount_in_rubles(transaction)
    assert(result, 0.0)


def test_get_transaction_amount_in_rubles_no_amount():
    """Тест для транзакции без суммы"""
    result = get_transaction_amount_in_rubles("invalid_transaction_no_amount")
    assert(result, 0.0)


def test_get_transaction_amount_in_rubles_no_currency_code():
    """Тест для транзакции без кода валюты"""
    result = get_transaction_amount_in_rubles("invalid_transaction_no_currency")
    assert(result, 0.0)


def test_get_transaction_amount_in_rubles_invalid_structure():
    """Тест для транзакции с невалидной структурой"""
    # Транзакция с невалидной вложенностью
    transaction = {
        "id": 8,
        "operationAmount": {
            "amount": "100.00",
            "currency": "RUB"  # Должен быть словарь, а не строка
        }
    }
    result = get_transaction_amount_in_rubles(transaction)
    assert(result, 0.0)
