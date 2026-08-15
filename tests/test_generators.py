"""Тесты функций модуля generators."""

from collections.abc import Iterator
from typing import Any

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize(
    ("currency", "expected_ids"),
    [
        ("USD", [939719570, 142264268, 895315941]),
        ("RUB", [873106923, 594226727]),
    ],
)
def test_filter_by_currency(transactions: list[dict[str, Any]], currency: str, expected_ids: list[int]) -> None:
    """Проверить фильтрацию транзакций по разным валютам."""
    result = filter_by_currency(transactions, currency)

    assert [transaction["id"] for transaction in result] == expected_ids


@pytest.mark.parametrize("currency", ["EUR", "usd"])
def test_filter_by_currency_without_matches(transactions: list[dict[str, Any]], currency: str) -> None:
    """Проверить отсутствие транзакций в запрошенной валюте."""
    assert list(filter_by_currency(transactions, currency)) == []


def test_filter_by_currency_returns_iterator(transactions: list[dict[str, Any]]) -> None:
    """Проверить, что функция возвращает итератор."""
    result = filter_by_currency(transactions, "USD")

    assert isinstance(result, Iterator)
    assert iter(result) is result


def test_filter_by_currency_yields_transactions_in_order(transactions: list[dict[str, Any]]) -> None:
    """Проверить последовательную выдачу транзакций и завершение итератора."""
    usd_transactions = filter_by_currency(transactions, "USD")

    assert next(usd_transactions)["id"] == 939719570
    assert next(usd_transactions)["id"] == 142264268
    assert next(usd_transactions)["id"] == 895315941

    with pytest.raises(StopIteration):
        next(usd_transactions)


def test_filter_by_currency_empty_list() -> None:
    """Проверить работу генератора с пустым списком."""
    assert list(filter_by_currency([], "USD")) == []


@pytest.mark.parametrize(
    "descriptions",
    [
        ["Перевод организации"],
        ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"],
        [],
    ],
)
def test_transaction_descriptions(descriptions: list[str]) -> None:
    """Проверить генератор на разных наборах описаний."""
    transactions: list[dict[str, Any]] = [{"description": description} for description in descriptions]

    assert list(transaction_descriptions(transactions)) == descriptions


def test_transaction_descriptions_returns_iterator(transactions: list[dict[str, Any]]) -> None:
    """Проверить, что функция возвращает итератор."""
    result = transaction_descriptions(transactions)

    assert isinstance(result, Iterator)
    assert iter(result) is result


def test_transaction_descriptions_yields_in_order(transactions: list[dict[str, Any]]) -> None:
    """Проверить последовательную выдачу описаний и завершение итератора."""
    descriptions = transaction_descriptions(transactions)

    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"
    assert next(descriptions) == "Перевод организации"

    with pytest.raises(StopIteration):
        next(descriptions)


def test_transaction_descriptions_without_description() -> None:
    """Проверить исключение при отсутствии ключа description."""
    descriptions = transaction_descriptions([{"id": 1}])

    with pytest.raises(KeyError, match="description"):
        next(descriptions)


@pytest.mark.parametrize(
    ("start", "stop", "expected"),
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (
            9999,
            10001,
            [
                "0000 0000 0000 9999",
                "0000 0000 0001 0000",
                "0000 0000 0001 0001",
            ],
        ),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
        (5, 4, []),
    ],
)
def test_card_number_generator(start: int, stop: int, expected: list[str]) -> None:
    """Проверить генерацию разных диапазонов номеров карт."""
    assert list(card_number_generator(start, stop)) == expected


def test_card_number_generator_returns_iterator() -> None:
    """Проверить, что функция возвращает итератор."""
    result = card_number_generator(start=1, stop=1)

    assert isinstance(result, Iterator)
    assert iter(result) is result


@pytest.mark.parametrize(
    "number",
    [1, 1234, 1234567890123456, 9999999999999999],
)
def test_card_number_generator_format(number: int) -> None:
    """Проверить формат из четырех групп по четыре цифры."""
    card_number = next(card_number_generator(start=number, stop=number))
    card_number_parts = card_number.split()

    assert len(card_number_parts) == 4
    assert all(len(part) == 4 for part in card_number_parts)
    assert all(part.isdigit() for part in card_number_parts)


def test_card_number_generator_stops_after_end() -> None:
    """Проверить завершение генератора после конечного значения."""
    card_numbers = card_number_generator(1, 2)

    assert next(card_numbers) == "0000 0000 0000 0001"
    assert next(card_numbers) == "0000 0000 0000 0002"

    with pytest.raises(StopIteration):
        next(card_numbers)
