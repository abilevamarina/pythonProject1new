# Проект 1

## Описание:

Проект 1 - это веб-приложение на Python для управления задачами и проектами

## Установка:

1. Клонируйте репозиторий:
``` shell
git clone https://github.com/abilevamarina/pythonProject1new.git
```
2. Установка зависимостей:
``` 
pip install -r requiremets.txt
```
## Использование:

1. Откройте приложение в вашем веб-браузере.
2. Создайте проект и начните добавлять задачи.
3. Назначайте сроки выполнения и приоритеты для задач, чтобы эффективно управлять проектами.

# Документация:

Для получения дополнительной информации, обратитесь к [документации](docs/README.md)

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).

## Тестирование

Обзор
Этот проект содержит комплексные тесты для функций обработки финансовых транзакций, включая маскировку данных, фильтрацию, сортировку и преобразование дат.

Установка и настройка
Требования
Python 3.7+

pytest

pytest-cov (для покрытия кода)

Установка зависимостей
bash
pip install pytest pytest-cov
Структура тестов
1. Тесты для функции mask_account_card
Назначение: Тестирование маскировки номеров карт и счетов

Тестируемые сценарии:

✅ Распознавание типа данных (карта vs счет)

✅ Параметризованные тесты для разных типов карт

✅ Маскировка счетов

✅ Автоматическое определение типа по длине номера

✅ Обработка некорректных входных данных

✅ Устойчивость к ошибкам

2.Тесты для функции get_date
Назначение: Тестирование преобразования форматов дат

Тестируемые сценарии:

✅ Преобразование стандартных ISO-форматов

✅ Граничные случаи (високосные года, границы месяцев)

✅ Нестандартные строки с датами

✅ Обработка различных форматов времени

✅ Сохранение ведущих нулей

3.Тесты для функции filter_by_state
Назначение: Тестирование фильтрации транзакций по статусу

Тестируемые сценарии:

✅ Фильтрация по разным состояниям (EXECUTED, PENDING, CANCELED)

✅ Обработка отсутствующего ключа state

✅ Пустые списки и граничные случаи

✅ Сохранение исходного списка

4. Тесты для функции sort_by_date
Назначение: Тестирование сортировки транзакций по дате

Тестируемые сценарии:

✅ Сортировка по убыванию и возрастанию

✅ Одинаковые даты (стабильность сортировки)

✅ Некорректные форматы дат

✅ Отсутствующие даты

✅ Разные форматы дат
Примеры тестов:

python
def test_card_masking()
def test_account_masking() 
def test_invalid_inputs()
def test_very_long_account_number()
def test_standard_date_formats()
def test_edge_cases()
def test_invalid_date_formats()
def sample_transactions()
def transactions_with_missing_state()
def test_filter_executed_default()
def test_filter_nonexistent_state()
def test_empty_list()
def test_missing_state_key()
def test_all_transactions_missing_state()
def test_filter_by_state_parametrized()
def sample_transaction()
def transactions_with_invalid_formats()
def test_sort_descending_default()
def test_sort_ascending_explicit()
def test_invalid_date_formats_descending()
def test_invalid_date_formats_ascending()
def test_specific_invalid_date_ordering()
def test_different_standard_formats()
def test_sort_direction_parametrized()
def test_various_scenarios_parametrized()
def test_get_mask_card_number_valid()
def test_get_mask_card_number_invalid()
def test_get_mask_account_valid()
def test_get_mask_account_invalid()
def test_get_mask_card_number_parametrized()
def test_get_mask_account_parametrized()


Запуск тестов
Базовый запуск
bash
pytest
Подробный вывод
bash
pytest -v
Запуск с покрытием кода
bash
pytest --cov=. --cov-report=term-missing
Запуск конкретных тестов
По имени файла:

bash
pytest test_functions.py -v
По классу тестов:

bash
pytest -v TestMaskAccountCard
pytest -v TestGetDate
pytest -v TestFilterByState  
pytest -v TestSortByDate
По конкретному методу:

bash
pytest -v TestMaskAccountCard::test_card_masking
pytest -v TestGetDate::test_standard_date_formats
По маркерам:

bash
pytest -m "parametrized" -v
Генерация отчетов
HTML отчет о покрытии:

bash
pytest --cov=. --cov-report=html
XML отчет (для CI):

bash
pytest --cov=. --cov-report=xml
Фикстуры
Проект использует pytest фикстуры для подготовки тестовых данных:

sample_transactions - примеры транзакций

transactions_with_same_dates - транзакции с одинаковыми датами

transactions_with_missing_dates - транзакции без дат

transactions_with_invalid_formats - транзакции с некорректными датами

Параметризованные тесты
Используется @pytest.mark.parametrize для тестирования множества сценариев:

python
@pytest.mark.parametrize("input_str,expected", [
    ("Visa Platinum 1234567812345678", "Visa Platinum 1234 56** **** 5678"),
    ("MasterCard 9999888877776666", "MasterCard 9999 88** **** 6666"),
])
def test_card_masking(self, input_str, expected):
Обработка исключений
Тесты проверяют корректную обработку ошибок:

python
def test_invalid_inputs(self, invalid_input, expected_exception):
    with pytest.raises(expected_exception):
        mask_account_card(invalid_input)
Интеграционные тесты
Включают тесты совместной работы функций:

python
def test_mask_account_card_with_date_processing(self):
    # Тестирование полного цикла обработки транзакции
Best Practices
Организация тестов
Каждый класс тестов соответствует одной функции

Четкие названия тестовых методов

Использование фикстур для переиспользуемых данных

Параметризация для избежания дублирования кода

Структура тестов
Setup - подготовка данных (фикстуры)

Execution - вызов тестируемой функции

Assertion - проверка результатов

Teardown - очистка (при необходимости)

Покрытие кода
Стремимся к 100% покрытию:

Основная функциональность

Граничные случаи

Обработка ошибок

Интеграционные сценарии

Troubleshooting
Common Issues
Импорт модулей:

python
# conftest.py
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
Отсутствующие зависимости:

bash
pip install -r requirements.txt
Проблемы с путями:

bash
python -m pytest
Debugging
Запуск с выводом print:

bash
pytest -s
Запуск конкретного теста с debug:

bash
pytest -x -v TestClass::test_method
Показать подробности о пропущенных тестах:

bash
pytest -rs
CI/CD Integration
Тесты могут быть интегрированы в CI/CD пайплайн:

yaml
# Пример .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
        with:
          file: ./coverage.xml

# Набор утилит для работы с банковскими транзакциями и генерации номеров карт.

## Функции
filter_by_currency
Фильтрует транзакции по заданной валюте и возвращает итератор.

python
def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]
Параметры:

transactions - список словарей с транзакциями

currency - валюта для фильтрации (например, 'USD', 'EUR', 'RUB')

Возвращает:

Итератор, который выдает транзакции с заданной валютой

Пример использования:

python
transactions = [
    {"id": 1, "amount": 100, "currency": "USD"},
    {"id": 2, "amount": 50, "currency": "EUR"},
    {"id": 3, "amount": 200, "currency": "USD"},
]

usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(transaction)
# Вывод: 
# {'id': 1, 'amount': 100, 'currency': 'USD'}
# {'id': 3, 'amount': 200, 'currency': 'USD'}
transaction_descriptions
Генератор, который возвращает описание каждой транзакции по очереди.

python
def transaction_descriptions(transactions: list[dict]) -> Iterator[str]
Параметры:

transactions - список словарей с транзакциями

Возвращает:

Итератор с описаниями транзакций

Пример использования:

python
transactions = [
    {"id": 1, "description": "Payment for services"},
    {"id": 2, "description": "Grocery shopping"},
    {"id": 3, "description": "Salary"},
]

descriptions = transaction_descriptions(transactions)
for desc in descriptions:
    print(desc)
# Вывод:
# Payment for services
# Grocery shopping
# Salary
card_number_generator
Генератор номеров банковских карт в заданном диапазоне.

python
def card_number_generator(start: int, end: int) -> Iterator[str]
Параметры:

start - начальный номер карты (от 1 до 9999999999999999)

end - конечный номер карты (от 1 до 9999999999999999)

Возвращает:

Итератор с номерами карт в формате "XXXX XXXX XXXX XXXX"

Пример использования:

python
card_numbers = card_number_generator(1, 5)
for card in card_numbers:
    print(card)
# Вывод:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005

## Тестирование
Запуск тестов
bash
# Запуск всех тестов
python bank_functions.py

# Или с использованием pytest
pytest test_bank_functions.py -v
Описание тестов
Тесты для filter_by_currency
test_filter_usd_transactions - фильтрация USD транзакций

test_filter_eur_transactions - фильтрация EUR транзакций

test_no_matching_currency - когда нет подходящих транзакций

test_empty_transactions_list - работа с пустым списком

test_transactions_without_currency_field - транзакции без поля currency

test_returns_iterator - проверка типа возвращаемого значения

Тесты для transaction_descriptions
test_extract_descriptions - извлечение описаний транзакций

test_empty_descriptions - работа с пустыми описаниями

test_missing_description_field - транзакции без поля description

test_mixed_transactions - смешанные транзакции

test_returns_generator - проверка типа возвращаемого значения

Тесты для card_number_generator
test_small_range - генерация небольшого диапазона

test_large_numbers - генерация больших номеров

test_middle_range - номера в середине диапазона

test_single_number - генерация одного номера

test_format_consistency - проверка формата вывода

test_returns_generator - проверка типа возвращаемого значения

Интеграционные тесты
test_combined_usage - совместное использование функций

test_performance_large_range - производительность на большом диапазоне

Пример тестовых данных
python
SAMPLE_TRANSACTIONS = [
    {
        "id": 939719570,
        "state": "EXECUTED", 
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952", 
        "to": "Счет 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878", 
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    }
]
## Требования
Python 3.6+

Для тестирования: pytest (опционально)

### Особенности
Ленивые вычисления - функции возвращают итераторы, экономя память

Безопасность - использование .get() для избежания KeyError

Типизация - правильные аннотации типов для статического анализа

Производительность - эффективная работа с большими объемами данных

### Примечания
Все функции работают с итераторами, что позволяет обрабатывать большие наборы данных

Для получения списка результатов используйте list()

Функции безопасно обрабатывают отсутствующие поля в словарях