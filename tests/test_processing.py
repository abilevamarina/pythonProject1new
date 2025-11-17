from src.processing import filter_by_state, sort_by_date
from tests.conftest import pytest


@pytest.fixture
def sample_transactions():
    """Фикстура с примером транзакций для тестирования"""
    return [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "EXECUTED", "amount": 200},
        {"id": 3, "state": "CANCELED", "amount": 400},
        {"id": 4, "state": "EXECUTED", "amount": 500},
    ]


@pytest.fixture
def transactions_with_missing_state():
    """Фикстура с транзакциями, где у некоторых отсутствует ключ state"""
    return [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "amount": 200},  # нет ключа state
        {"id": 3, "amount": 400},  # нет ключа state
        {"id": 4, "state": "EXECUTED", "amount": 500},
    ]


def test_filter_executed_default(sample_transactions):
    """Тест фильтрации по умолчанию (EXECUTED)"""
    result = filter_by_state(sample_transactions)

    assert all(transaction["state"] == "EXECUTED" for transaction in result)
    assert result[0]["id"] == 1
    assert result[2]["id"] == 4


def test_filter_nonexistent_state(sample_transactions):
    """Тест фильтрации по несуществующему состоянию"""
    result = filter_by_state(sample_transactions, "COMPLETED")

    assert len(result) == 0
    assert result == []


def test_empty_list():
    """Тест с пустым списком транзакций"""
    result = filter_by_state([])
    assert result == []


def test_missing_state_key(transactions_with_missing_state):
    """Тест с транзакциями, где у некоторых отсутствует ключ state"""
    result = filter_by_state(transactions_with_missing_state, "EXECUTED")

    assert len(result) == 2
    assert all(transaction["state"] == "EXECUTED" for transaction in result)
    assert result[0]["id"] == 1
    assert result[1]["id"] == 4


def test_all_transactions_missing_state():
    """Тест когда у всех транзакций отсутствует ключ state"""
    transactions = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200},
    ]

    result = filter_by_state(transactions, "EXECUTED")
    assert result == []


# Параметризация
@pytest.mark.parametrize(
    "state,expected_count,expected_ids",
    [
        ("EXECUTED", 3, [1, 2, 4]),
        ("COMPLETED", 0, []),
    ],
)
def test_filter_by_state_parametrized(
    sample_transactions, state, expected_count, expected_ids
):
    result = filter_by_state(sample_transactions, state)

    assert len(result) == expected_count
    assert [i["id"] for i in result] == expected_ids


@pytest.fixture
def sample_transaction():
    """Фикстура с примером транзакций для тестирования по датам"""
    return [
        {"id": 1, "date": "2025-01-15", "amount": 100},
        {"id": 2, "date": "2025-03-20", "amount": 200},
        {"id": 3, "date": "2025-01-10", "amount": 300},
        {"id": 4, "date": "2025-02-05", "amount": 400},
        {"id": 5, "date": "2025-03-01", "amount": 500},
    ]


@pytest.fixture
def transaction_with_invalid_formats():
    """Фикстура с транзакциями с некорректными или нестандартными форматами дат"""
    return [
        {"id": 1, "date": "2025-01-15", "amount": 100},  # Корректный формат
        {"id": 2, "date": "invalid-date-here", "amount": 200},  # Некорректная дата
        {"id": 3, "date": "15.01.2025", "amount": 300},  # Корректный формат
        {"id": 4, "date": "2025/12/31", "amount": 400},  # Возможный формат
        {"id": 5, "date": "01-15-2025", "amount": 500},  # Допустимый формат
        {"id": 6, "date": "", "amount": 600},  # Пустая строка
        {"id": 7, "date": "20230115", "amount": 700},  # Без разделителей
        {"id": 8, "date": "31-Дек-2025", "amount": 800},  # Месяц текстом
    ]


# ТЕСТ 1: Сортировка по убыванию
def test_sort_descending_default(sample_transaction):
    """Тестирование сортировки по датам в порядке убывания"""
    result = sort_by_date(sample_transaction)

    expected_dates = [
        "2025-03-20",
        "2025-03-01",
        "2025-02-05",
        "2025-01-15",
        "2025-01-10",
    ]
    actual_dates = [transaction["date"] for transaction in result]

    assert actual_dates == expected_dates
    assert result[0]["id"] == 2  # Самая поздняя дата
    assert result[-1]["id"] == 3  # Самая ранняя дата


# ТЕСТ 2: Сортировка по возрастанию
def test_sort_ascending_explicit(sample_transaction):
    """Тестирование сортировки по датам в порядке возрастания"""
    result = sort_by_date(sample_transaction, descending=False)

    expected_dates = [
        "2025-01-10",
        "2025-01-15",
        "2025-02-05",
        "2025-03-01",
        "2025-03-20",
    ]
    actual_dates = [transaction["date"] for transaction in result]

    assert actual_dates == expected_dates
    assert result[0]["id"] == 3  # Самая ранняя дата
    assert result[-1]["id"] == 2  # Самая поздняя дата


# ТЕСТ 3: Работа с некорректными форматами дат
def test_invalid_date_formats_descending(transaction_with_invalid_formats):
    """Тестирование сортировки с некорректными форматами дат (убывание)"""
    result = sort_by_date(transaction_with_invalid_formats, descending=True)

    # Некорректные даты сортируются как обычные строки
    actual_dates = [transaction["date"] for transaction in result]

    assert actual_dates == sorted(actual_dates, reverse=True)


def test_invalid_date_formats_ascending(transaction_with_invalid_formats):
    """Тестирование сортировки с некорректными форматами дат (возрастание)"""
    result = sort_by_date(transaction_with_invalid_formats, descending=False)

    actual_dates = [transaction["date"] for transaction in result]

    assert actual_dates == sorted(actual_dates, reverse=False)


def test_specific_invalid_date_ordering():
    """Тестирование конкретного порядка некорректных дат"""
    transaction = [
        {"id": 1, "date": "2025-01-15", "amount": 100},  # Корректная дата
        {"id": 2, "date": "invalid", "amount": 200},  # Некорректная
        {"id": 3, "date": "", "amount": 300},  # Пустая строка
        {"id": 4, "date": "abc", "amount": 400},  # Некорректная
    ]

    result = sort_by_date(transaction, descending=True)
    # В убывающем порядке: корректные даты -> некорректные
    assert len(result) == 4
    assert set(t["id"] for t in result) == {1, 2, 3, 4}


def test_different_standard_formats():
    """Тестирование с разными стандартными форматами дат"""
    transaction = [
        {"id": 1, "date": "2025-12-31", "amount": 100},
        {"id": 2, "date": "31.12.2025", "amount": 200},
        {"id": 3, "date": "12/31/2025", "amount": 300},
        {"id": 4, "date": "20251231", "amount": 400},
    ]

    result = sort_by_date(transaction, descending=True)
    # Сортировка
    actual_dates = [i["date"] for i in result]
    actual_ids = [i["id"] for i in result]

    # Ожидаемый порядок
    assert actual_dates == ['31.12.2025', '20251231', '2025-12-31', '12/31/2025']


# Параметизация
@pytest.mark.parametrize(
    "descending,expected_ids",
    [
        (True, [2, 5, 4, 1, 3]),  # по убыванию
        (False, [3, 1, 4, 5, 2]),  # по возрастанию
    ],
)
def test_sort_direction_parametrized(sample_transaction, descending, expected_ids):
    """направление сортировки"""
    result = sort_by_date(sample_transaction, descending=descending)
    assert [i["id"] for i in result] == expected_ids


@pytest.mark.parametrize(
    "transaction,expected_desc,expected_asc",
    [
        # Пустой список
        ([], [], []),
        # Один элемент
        ([{"id": 1, "date": "2025-01-01"}], [1], [1]),
        # Все даты одинаковые
        (
            [
                {"id": 1, "date": "2025-01-01"},
                {"id": 2, "date": "2025-01-01"},
                {"id": 3, "date": "2025-01-01"},
            ],
            [1, 2, 3],
            [1, 2, 3],
        ),
        # Только некорректные даты
        (
            [
                {"id": 1, "date": "invalid"},
                {"id": 2, "date": "wrong"},
                {"id": 3, "date": "error"},
            ],
            [2, 1, 3],
            [3, 1, 2],
        ),  # сортировка
    ],
)
def test_various_scenarios_parametrized(transaction, expected_desc, expected_asc):
    """тестирование различных сценариев"""
    result_desc = sort_by_date(transaction, descending=True)
    result_asc = sort_by_date(transaction, descending=False)

    assert [i["id"] for i in result_desc] == expected_desc
    assert [i["id"] for i in result_asc] == expected_asc
