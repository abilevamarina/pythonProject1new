import os
import requests
from typing import Dict, Any
from decimal import Decimal, ROUND_HALF_UP


# Константы для валютных кодов
RUB_CURRENCY = "RUB"
USD_CURRENCY = "USD"
EUR_CURRENCY = "EUR"

# URL для API курсов валют
EXCHANGE_RATE_API_URL = " https://apilayer.com/exchangerates_data-api"


def get_exchange_rate(from_currency: str, to_currency: str = RUB_CURRENCY) -> float:
    """
    Получает текущий курс обмена валюты к рублям через внешнее API.
    """
    try:
        # Получаем API ключ из переменных окружения
        api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        if not api_key:
            print("API ключ не найден в переменных окружения")
            return 0.0

        #запросы
        headers = {
            "apikey": api_key
        }
        # Параметры запроса
        params = {
            "base": from_currency,
            "symbols": to_currency
        }

        # Выполняем запрос к API
        response = requests.get(
            EXCHANGE_RATE_API_URL,
            headers=headers,
            params=params,
            timeout=10  # Таймаут 10 секунд
        )

        # Проверяем статус ответа
        response.raise_for_status()

        # JSON ответ
        data = response.json()

        # Извлекаем курс обмена
        rate = data.get("rates", {}).get(to_currency, 0.0)

        return float(rate)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API курсов валют: {e}")
        return 0.0
    except (KeyError, ValueError) as e:
        print(f"Ошибка при обработке ответа API: {e}")
        return 0.0
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return 0.0


def convert_to_rubles(amount_str: str, currency_code: str) -> float:
    """
     Конвертирует сумму из указанной валюты в рубли.
    """
    try:
        # Преобразуем строку суммы в Decimal для точности
        amount_decimal = Decimal(amount_str)

        # Если валюта уже в рублях, возвращаем как есть
        if currency_code == RUB_CURRENCY:
            return float(amount_decimal)

        # Если валюта USD или EUR, конвертируем
        if currency_code in (USD_CURRENCY, EUR_CURRENCY):
            # Получаем курс обмена
            exchange_rate = get_exchange_rate(currency_code, RUB_CURRENCY)

            if exchange_rate <= 0:
                print(f"Не удалось получить курс для {currency_code}")
                return 0.0

            # Конвертируем сумму
            converted_amount = amount_decimal * Decimal(str(exchange_rate))

            # Округляем до 2 знаков после запятой как для денег
            rounded_amount = converted_amount.quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
            )

            return float(rounded_amount)

        return float(amount_decimal)

    except Exception as e:
        print(f"Ошибка при конвертации суммы: {e}")
        return 0.0


def get_transaction_amount_in_rubles(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях.
    """

    try:
        # Извлекаем данные о сумме операции
        operation_amount = transaction.get("operationAmount", {})

        if not operation_amount:
            print("Не найдены данные о сумме операции")
            return 0.0

        # Получаем сумму и валюту
        amount_str = operation_amount.get("amount")
        currency = operation_amount.get("currency", {})
        currency_code = currency.get("code")

        if not amount_str or not currency_code:
            print("Не найдена сумма или код валюты")
            return 0.0

        # Конвертируем в рубли
        return convert_to_rubles(amount_str, currency_code)
    except Exception as e:
        print(f"Ошибка при обработке транзакции: {e}")
        return 0.0
