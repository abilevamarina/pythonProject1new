import json
import os
from typing import List, Dict, Any
from src.external_api.py import get_transaction_amount_in_rubles


def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            return []

        # Проверяем, не пустой ли файл
        if os.path.getsize(file_path) == 0:
            return []

        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, IOError):
        # Если возникла ошибка при чтении
        return []

def get_amount_in_rubles(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях.
    """
    from external_api import get_transaction_amount_in_rubles
    return get_transaction_amount_in_rubles(transaction)
