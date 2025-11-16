import pytest
from src.widget import mask_account_card, get_date


# Параметизация
@pytest.mark.parametrize("input_str,expected", [
    # Visa/MasterCard карты
    ("Visa Platinum 1234567812345678", "Visa Platinum 1234 56** **** 5678"),
    ("MasterCard 9999888877776666", "MasterCard 9999 88** **** 6666"),
    ("МИР 1234123412341234", "МИР 1234 12** **** 1234"),
    ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
    # Карты с пробелами в номере
    ("Visa Classic 1234 5678 1234 5678", "Visa Classic 1234 56** **** 5678"),
    ("Card 1234-5678-1234-5678", "Card 1234 56** **** 5678"),
])
def test_card_masking(input_str, expected):
    """Тестирование маскировки номеров карт"""
    result = mask_account_card(input_str)
    assert result == expected

@pytest.mark.parametrize("input_str,expected", [
        # Счета
        ("Счет 12345678901234567890", "Счет **7890"),
        ("счет 98765432109876543210", "счет **3210"),
        ("Расчетный счет 11112222333344445555", "Расчетный счет **5555"),
        # Счета с разделителями
        ("Счет 1234-5678-9012-3456-7890", "Счет **7890"),
        ("Account 12345678901234567899", "Account **7899"),
    ])
def test_account_masking(input_str, expected):
    """Тестирование маскировки номеров счетов"""
    result = mask_account_card(input_str)
    assert result == expected

# Тесты для некорректных входных данных
@pytest.mark.parametrize("invalid_input,expected_exception", [
        ("", ""),  # Пустая строка
        ("Visa", ValueError),  # Только тип
        ("1234567890123456", ValueError),  # Только номер
        ("Visa Platinum", ValueError),  # Тип без номера
        ("Visa Platinum abcdef", ValueError),  # Нет цифр
        ("Visa Platinum 1234", ValueError),  # Слишком короткий для карты
("Visa Platinum 123456789012345", ValueError),  # 15 цифр для карты
    ])
def test_invalid_inputs(invalid_input, expected_exception):
    """Тестирование обработки некорректных входных данных"""
    if expected_exception == "":
        result = mask_account_card(invalid_input)
        assert result == ""
    else:
        with pytest.raises(expected_exception):
            mask_account_card(invalid_input)

def test_very_long_account_number():
    """Тестирование очень длинных номеров счетов"""
    long_account = "1" * 30  # 30 цифр
    result = mask_account_card(f"Счет {long_account}")
    assert result == f"Счет **{long_account[-4:]}"


"""Тесты для функции get_date"""
# Параметризованные тесты для стандартных форматов даты
@pytest.mark.parametrize("input_date,expected", [
        ("2025-12-31T10:30:00", "31.12.2023"),
        ("2025-01-01T00:00:00", "01.01.2023"),
        ("2025-12-31T12:00:00", "31.12.2025"),
        ("2030-06-15T15:45:30", "15.06.2030"),
])
def test_standard_date_formats(input_date, expected):
    """Тестирование преобразования стандартных форматов даты"""
    result = get_date(input_date)
    assert result == expected

@pytest.mark.parametrize("input_date,expected", [
        ("2025-01-01", "01.01.2025"),  # Без времени
        ("2025-12-31T", "31.12.2025"),  # Пустое время
        ("2025-06-15T10:30", "15.06.2025"),  # Время без секунд
    ])
def test_edge_cases(input_date, expected):
        """Тестирование различных случаев"""
        result = get_date(input_date)
        assert result == expected


# Тесты для обработки ошибок
@pytest.mark.parametrize("invalid_date", [
    "",  # Пустая строка
    "invalid-date",  # Неправильный формат
    "2025-13-01T10:30:00",  # Неправильный месяц
    "2025-12-32T10:30:00",  # Неправильный день
    "2025-12-31T25:30:00",  # Неправильный час
 ])
def test_invalid_date_formats(invalid_date):
    """Тестирование обработки некорректных форматов даты"""
    try:
        result = get_date(invalid_date)
        # Если функция не вызвала исключение, проверяем корректность результата
        assert isinstance(result, str)
        # Проверяем базовый формат ДД.ММ.ГГГГ
        if result:
            parts = result.split('.')
            assert len(parts) == 3
            assert len(parts[0]) == 2  # День
            assert len(parts[1]) == 2  # Месяц
            assert len(parts[2]) == 4  # Год
    except (ValueError, IndexError):
        # Ожидаем исключение для некорректных форматов
        pass