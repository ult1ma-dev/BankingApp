"""Функции для маскировки банковских реквизитов."""

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Вернуть замаскированный номер банковской карты."""
    logger.debug("Начало маскировки номера банковской карты")

    try:
        masked_number = f"{card_number[:6]}******{card_number[-4:]}"
        result = " ".join(masked_number[index : index + 4] for index in range(0, 16, 4))
    except TypeError as error:
        logger.error("Ошибка при маскировке номера банковской карты: %s", error)
        raise

    logger.info("Номер банковской карты успешно замаскирован: %s", result)
    return result


def get_mask_account(account_number: str) -> str:
    """Вернуть замаскированный номер банковского счёта, последние 4 цифры."""
    logger.debug("Начало маскировки номера банковского счёта")

    try:
        result = f"**{account_number[-4:]}"
    except TypeError as error:
        logger.error("Ошибка при маскировке номера банковского счёта: %s", error)
        raise

    logger.info("Номер банковского счёта успешно замаскирован: %s", result)
    return result
