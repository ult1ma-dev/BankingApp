"""Генераторы для обработки банковских транзакций."""

from collections.abc import Iterator
from typing import Any


def filter_by_currency(transactions: list[dict[str, Any]], currency: str) -> Iterator[dict[str, Any]]:
    """Поочередно возвращать транзакции в указанной валюте."""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
    """Поочередно возвращать описания транзакций."""
    for transaction in transactions:
        yield str(transaction["description"])


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генерировать номера банковских карт в заданном диапазоне."""
    for number in range(start, stop + 1):
        number_as_string = str(number)
        number_of_zeros = 16 - len(number_as_string)
        card_number = "0" * number_of_zeros + number_as_string

        first_part = card_number[0:4]
        second_part = card_number[4:8]
        third_part = card_number[8:12]
        fourth_part = card_number[12:16]

        yield first_part + " " + second_part + " " + third_part + " " + fourth_part
