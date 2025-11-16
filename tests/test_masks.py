import pytest
from src.masks import get_mask_account, get_mask_card_number


def test_one():
    assert 1 == 1


def new_changes():
    pass


def test_get_mask_card_number_valid():
    """Тест маскировки номера карты с возможными данными"""
    assert get_mask_card_number(1234567890123456) == "1234 56** **** 3456"


def test_get_mask_card_number_invalid():
    """Тест маскировки номера карты с ошибочными данными"""
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number(12345678901234)  # 14 цифр

    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number(12345678901234567)  # 17 цифр


def test_get_mask_account_valid():
    """Тест маскировки номера счета с возможными данными"""
    assert get_mask_account(1234567890) == "**7890"
    assert get_mask_account(1234) == "**1234"
    assert get_mask_account(100005000) == "**5000"
    assert get_mask_account(12345678901234567890) == "**7890"


def test_get_mask_account_invalid():
    """Тест маскировки номера счета с ошибочными данными"""
    with pytest.raises(
        ValueError, match="Номер счета должен содержать минимум 4 цифры"
    ):
        get_mask_account(123)  # 3 цифры

    with pytest.raises(
        ValueError, match="Номер счета должен содержать минимум 4 цифры"
    ):
        get_mask_account(1)  # 1 цифра

"""Параметизация"""
@pytest.mark.parametrize("input_card,expected", [
    (1234567890123456, "1234 56** **** 3456"),
])
def test_get_mask_card_number_parametrized(self, input_card, expected):
    assert get_mask_card_number(input_card) == expected


@pytest.mark.parametrize("input_account,expected", [
    (1234567890, "**7890"),
    (1234, "**1234"),
    (100005000, "**5000"),
    (9999999999, "**9999"),
])
def test_get_mask_account_parametrized(input_account, expected):
     assert get_mask_account(input_account) == expected