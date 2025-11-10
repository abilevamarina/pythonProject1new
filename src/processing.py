def filter_by_state(transactions, state='EXECUTED'):
    """
    Фильтрует список словарей по значению ключа "state"
    """
    filtered_list = []

    for transaction in transactions:
        # Проверяем, что словарь содержит ключ "state"
        if transaction.get("state") == state:
            filtered_list.append(transaction)

    return filtered_list