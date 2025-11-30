from typing import Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """
    Фильтрует транзакции по заданной валюте.
    """
    return (
        transaction
        for transaction in transactions
        if transaction.get("currency") == currency
    )


def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """
    Генератор, который возвращает описание каждой транзакции по очереди.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в заданном диапазоне.
    """
    for number in range(start, stop + 1):
        # Преобразуем в строку и дополняем нулями
        card_str = str(number)
        if len(card_str) < 16:
            card_str = "0" * (16 - len(card_str)) + card_str

        # Форматируем в группы по 4 цифры
        formatted_card = (
            f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        )

        yield formatted_card
