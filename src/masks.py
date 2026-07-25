"""Функции для маскировки банковских реквизитов."""


def get_mask_card_number(card_number: str) -> str:
    """Вернуть замаскированный номер банковской карты."""
    masked_number = f"{card_number[:6]}******{card_number[-4:]}"
    return " ".join(masked_number[index : index + 4] for index in range(0, 16, 4))


def get_mask_account(account_number: str) -> str:
    """Вернуть замаскированный номер банковского счёта, последние 4 цифры."""
    return f"**{account_number[-4:]}"
