def get_mask_card_number(card_number: int) -> str:
    """Маскируем номер карты по формату"""
    """XXXX XX** **** XXXX"""
    card_str = str(card_number).replace(" ", "")

    if len(card_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
    """Форматируем: первые 6, затем маскируем 6,"""
    """показываем последние 4 цифры"""
    return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"


def get_mask_account(account_number: int) -> str:
    """Маскируем номер счета по формату **XXXX"""
    account_str = str(account_number)

    if len(account_str) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")
    """Показываем только последние 4 цифры"""
    return f"**{account_str[-4:]}"
