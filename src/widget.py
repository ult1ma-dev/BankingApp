"""Функции для обработки банковских реквизитов."""

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_number_and_type: str) -> str:
    """Вернуть название карты или счета с замаскированным номером."""
    card_data = card_number_and_type.split()
    number = card_data[-1]
    name = " ".join(card_data[:-1])

    if name == "Счет":
        return name + " " + get_mask_account(number)
    else:
        return name + " " + get_mask_card_number(number)


def get_date(date_string: str) -> str:
    """Вернуть дату в формате ДД.ММ.ГГГГ."""
    year = date_string[0:4]
    month = date_string[5:7]
    day = date_string[8:10]

    return day + "." + month + "." + year
