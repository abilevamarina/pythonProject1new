def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает скрытый номер карты в формате XXXX XX** **** XXXX
    """
    # Убираем все пробелы и нецифровые символы
    cleaned_number = "".join(filter(str.isdigit, card_number))

    if len(cleaned_number) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр")

    # Форматируем: первые 6, затем маскируем 6, показываем последние 4
    return f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Возвращает замаскированный номер аккаунта в формате **XXXX
    """
    # Убираем все пробелы и нецифровые символы
    cleaned_number = "".join(filter(str.isdigit, account_number))

    if len(cleaned_number) < 4:
        raise ValueError("Номер счета должет состоять минимум из 4 цифр")

    # Показываем только последние 4 цифры
    return f"**{cleaned_number[-4:]}"


def mask_account_card(account_card_info: str) -> str:
    """ Возвращает cтроку с замаскированным числом и типом """
    if not account_card_info:
        return ""

    # Разделяем строку на слова
    words = account_card_info.split()

    if len(words) < 2:
        raise ValueError("Input string must contain at least type and number")

    # Извлекаем номер (последнее слово)
    number_part = words[-1]

    # Извлекаем тип (все слова кроме последнего)
    type_part = " ".join(words[:-1])

    # Очищаем номер от нецифровых символов
    cleaned_number = "".join(filter(str.isdigit, number_part))

    if not cleaned_number:
        raise ValueError("Нужно ввести цифры")

    # Определяем тип по ключевым словам и длине номера
    if "счет" in account_card_info.lower() or len(cleaned_number) > 16:
        # Обрабатываем как счет
        masked_number = get_mask_account(cleaned_number)
    else:
        # Обрабатываем как карту
        if len(cleaned_number) != 16:
            raise ValueError("Номер карты должен состоять из 16 цифр")
        masked_number = get_mask_card_number(cleaned_number)

    return f"{type_part} {masked_number}"

    if len(words) < 2:
        raise ValueError("В строке должно быть указано тип и номер")
    number_part = words[-1]
    type_part = " ".join(words[:-1])
    cleaned_number = "".join(filter(str.isdigit, number_part))

    if not cleaned_number:
        raise ValueError("Нужно ввести цифры")
    if "счет" in account_card_info.lower() or len(cleaned_number) > 16:
        masked_number = get_mask_account(cleaned_number)
    else:
        if len(cleaned_number) != 16:
            raise ValueError("Номер карты должен содержать 16 цифр")
        masked_number = get_mask_card_number(cleaned_number)

        return f"{type_part} {masked_number}"

def get_date(date_string: str) -> str:
    date_part = date_string.split('T')[0]
    year, month, day = date_part.split('-')

    # Форматируем в нужный формат ДД.ММ.ГГГГ
    return f"{day}.{month}.{year}"
