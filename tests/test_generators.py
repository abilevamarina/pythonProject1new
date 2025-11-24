from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)
from tests.conftest import pytest


"""Тесты для filter_by_currency"""


def test_filter_usd_transactions():
    """Тест фильтрации USD транзакций"""
    transactions = [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 50, "currency": "EUR"},
        {"id": 3, "amount": 200, "currency": "USD"},
    ]

    result = list(filter_by_currency(transactions, "USD"))
    expected = [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 3, "amount": 200, "currency": "USD"},
    ]

    assert result == expected


def test_filter_eur_transactions():
    """Тест фильтрации EUR транзакций"""
    transactions = [
        {"id": 1, "currency": "EUR"},
        {"id": 2, "currency": "USD"},
        {"id": 3, "currency": "EUR"},
    ]

    result = list(filter_by_currency(transactions, "EUR"))
    expected = [
        {"id": 1, "currency": "EUR"},
        {"id": 3, "currency": "EUR"},
    ]

    assert result == expected


@pytest.fixture
def sample_transactions():
    """Фикстура с примером транзакций для тестов"""
    return [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 50, "currency": "EUR"},
        {"id": 3, "amount": 200, "currency": "USD"},
        {"id": 4, "amount": 150, "currency": "EUR"},
    ]


@pytest.mark.parametrize("currency,expected_ids", [
    ("USD", [1, 3]),
    ("EUR", [2, 4]),
    ("JPY", []),  # Тест для валюты, которой нет в списке
])
def test_filter_by_currency(sample_transactions, currency, expected_ids):
    """Параметризованный тест фильтрации транзакций по валюте"""
    result = list(filter_by_currency(sample_transactions, currency))

    # Проверяем, что отфильтрованы правильные транзакции
    assert len(result) == len(expected_ids)
    assert all(tx["currency"] == currency for tx in result)
    assert [tx["id"] for tx in result] == expected_ids


@pytest.mark.parametrize("currency,expected_ids", [
    ("USD", [2]),
    ("EUR", [1, 3]),
])
def test_filter_transactions_without_amount(transactions_without_amount, currency, expected_ids):
    """Тест фильтрации транзакций без поля amount"""
    result = list(filter_by_currency(transactions_without_amount, currency))

    assert len(result) == len(expected_ids)
    assert all(tx["currency"] == currency for tx in result)
    assert [tx["id"] for tx in result] == expected_ids


def test_returns_iterator():
    """Тест, что функция возвращает итератор"""
    transactions = [{"id": 1, "currency": "USD"}]
    result = filter_by_currency(transactions, "USD")

    # Проверяем что можно использовать next
    assert hasattr(result, "__iter__")
    assert next(result) == {"id": 1, "currency": "USD"}


"""Тесты для transaction_descriptions"""


def test_extract_descriptions():
    """Тест извлечения описаний транзакций"""
    transactions = [
        {"id": 1, "description": "Оплата услуг"},
        {"id": 2, "description": "Покупка продуктов"},
        {"id": 3, "description": "Зарплата"},
    ]

    result = list(transaction_descriptions(transactions))
    expected = ["Оплата услуг", "Покупка продуктов", "Зарплата"]

    assert result == expected


def test_empty_descriptions():
    """Тест с пустыми описаниями"""
    transactions = [
        {"id": 1, "description": ""},
        {"id": 2, "description": ""},
    ]

    result = list(transaction_descriptions(transactions))
    expected = ["", ""]

    assert result == expected


@pytest.fixture
def sample_transactions_with_descriptions():
    """Фикстура с транзакциями с описаниями"""
    return [
        {"id": 1, "description": "Оплата услуг", "amount": 100, "currency": "USD"},
        {"id": 2, "description": "Покупка продуктов", "amount": 50, "currency": "EUR"},
        {"id": 3, "description": "Зарплата", "amount": 200, "currency": "USD"},
        {"id": 4, "description": "Перевод другу", "amount": 75, "currency": "GBP"},
        {"id": 5, "description": "Оплата ЖКХ", "amount": 150, "currency": "EUR"},
    ]


@pytest.fixture
def transactions_with_empty_descriptions():
    """Фикстура с транзакциями с пустыми описаниями"""
    return [
        {"id": 1, "description": ""},
        {"id": 2, "description": ""},
        {"id": 3, "description": "", "amount": 100},
    ]


@pytest.mark.parametrize("expected_descriptions", [
    (["Оплата услуг", "Покупка продуктов", "Зарплата", "Перевод другу", "Оплата ЖКХ"]),
])
def test_extract_descriptions(sample_transactions_with_descriptions, expected_descriptions):
    """Параметризованный тест извлечения описаний транзакций"""
    result = list(transaction_descriptions(sample_transactions_with_descriptions))
    assert result == expected_descriptions

@pytest.mark.parametrize("expected_descriptions", [
    (["", "", ""]),])


def test_empty_descriptions(transactions_with_empty_descriptions, expected_descriptions):
    """Тест с пустыми описаниями"""
    result = list(transaction_descriptions(transactions_with_empty_descriptions))
    assert result == expected_descriptions


def test_returns_generator():
    """Тест, что функция возвращает генератор"""
    transactions = [{"id": 1, "description": "Test"}]
    result = transaction_descriptions(transactions)

    # Проверяем что это генератор
    assert hasattr(result, "__iter__")
    assert next(result) == "Test"


"""Тесты для card_number_generator"""


def test_small_range():
    """Тест генерации небольшого диапазона"""
    result = list(card_number_generator(1, 3))
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
    ]

    assert result == expected


@pytest.fixture
def small_range():
    """Фикстура для небольшого диапазона"""
    return 1, 3


def test_middle_range():
    """Тест генерации номеров в середине диапазона"""
    result = list(card_number_generator(1234567890123456, 1234567890123458))
    expected = [
        "1234 5678 9012 3456",
        "1234 5678 9012 3457",
        "1234 5678 9012 3458",
    ]

    assert result == expected

@pytest.fixture
def middle_range():
    """Фикстура для среднего диапазона"""
    return 1234567890123456, 1234567890123458


def test_format_consistency():
    """Тест формата вывода"""
    numbers = list(card_number_generator(1, 1))
    card_number = numbers[0]

    # Проверяем формат XXXX XXXX XXXX XXXX
    assert len(card_number) == 19  # 16 цифр + 3 пробела
    assert card_number[4] == " "
    assert card_number[9] == " "
    assert card_number[14] == " "

    # Проверяем что все символы до пробелов - цифры
    parts = card_number.split()
    assert len(parts) == 4
    assert all(part.isdigit() for part in parts)
    assert all(len(part) == 4 for part in parts)


@pytest.mark.parametrize("start,stop,expected", [
    (1, 3, [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
    ]),
    (1234567890123456, 1234567890123458, [
        "1234 5678 9012 3456",
        "1234 5678 9012 3457",
        "1234 5678 9012 3458",
    ]),
    (9999999999999998, 9999999999999999, [
        "9999 9999 9999 9998",
        "9999 9999 9999 9999",
    ]),
    (0, 1, [
        "0000 0000 0000 0000",
        "0000 0000 0000 0001",
    ]),
    (42, 42, [
        "0000 0000 0000 0042",
    ]),])
def test_card_number_generator(start, stop, expected):
    """Параметризованный тест генерации номеров карт"""
    result = list(card_number_generator(start, stop))
    assert result == expected


@pytest.mark.parametrize("start,stop", [
    (1, 5),
    (100, 104),
    (9999999999999995, 9999999999999999),
])
def test_format_consistency(start, stop):
    """Параметризованный тест формата вывода"""
    numbers = list(card_number_generator(start, stop))

    for card_number in numbers:
        # Проверяем формат XXXX XXXX XXXX XXXX
        assert len(card_number) == 19  # 16 цифр + 3 пробела
        assert card_number[4] == " "
        assert card_number[9] == " "
        assert card_number[14] == " "

        # Проверяем что все символы до пробелов - цифры
        parts = card_number.split()
        assert len(parts) == 4
        assert all(part.isdigit() for part in parts)
        assert all(len(part) == 4 for part in parts)


def test_return_generator():
    """Тест, что функция возвращает генератор"""
    result = card_number_generator(1, 5)

    # Проверяем что это генератор
    assert hasattr(result, "__iter__")
    first_number = next(result)
    assert first_number == "0000 0000 0000 0001"
