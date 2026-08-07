"""Тесты функций модуля widget."""

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    ("account_card", "expected"),
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(account_card: str, expected: str) -> None:
    """Проверить выбор маски для разных карт и счетов."""
    assert mask_account_card(account_card) == expected


@pytest.mark.parametrize(
    ("account_card", "error_message"),
    [
        ("", "не должна быть пустой"),
        ("   ", "не должна быть пустой"),
        ("Visa", "название и номер"),
        ("Visa Platinum not-a-number", "только из цифр"),
        ("Счет 1234", "20 цифр"),
        ("Visa Gold 1234", "16 цифр"),
    ],
)
def test_mask_account_card_invalid_input(account_card: str, error_message: str) -> None:
    """Проверить исключения для некорректных реквизитов."""
    with pytest.raises(ValueError, match=error_message):
        mask_account_card(account_card)


@pytest.mark.parametrize(
    ("date_string", "expected"),
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2000-02-29T23:59:59", "29.02.2000"),
        ("2024-01-01", "01.01.2024"),
        ("2024-12-31T23:59:59+03:00", "31.12.2024"),
        ("20240311T022618", "11.03.2024"),
    ],
)
def test_get_date(date_string: str, expected: str) -> None:
    """Проверить преобразование корректных ISO-дат."""
    assert get_date(date_string) == expected


@pytest.mark.parametrize(
    "date_string",
    ["", "not-a-date", "2024-02-30T12:00:00", "2024-13-01T00:00:00"],
)
def test_get_date_invalid_input(date_string: str) -> None:
    """Проверить исключение для пустых и некорректных дат."""
    with pytest.raises(ValueError):
        get_date(date_string)
