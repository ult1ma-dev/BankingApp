"""Функции для обработки банковских реквизитов."""

from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_number_and_type: str) -> str:
    """Вернуть название карты или счета с замаскированным номером."""
    if not card_number_and_type.strip():
        raise ValueError("Строка с названием и номером не должна быть пустой.")

    card_data = card_number_and_type.rsplit(maxsplit=1)

    if len(card_data) != 2:
        raise ValueError("Введите название и номер через пробел.")

    name = card_data[0]
    number = card_data[1]

    if not number.isdigit():
        raise ValueError("Номер должен состоять только из цифр.")

    if name == "Счет" and len(number) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр.")

    if name != "Счет" and len(number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр.")

    if name == "Счет":
        return name + " " + get_mask_account(number)
    else:
        return name + " " + get_mask_card_number(number)


def get_date(date_string: str) -> str:
    """Вернуть дату в формате ДД.ММ.ГГГГ."""
    date = datetime.fromisoformat(date_string)

    return date.strftime("%d.%m.%Y")
