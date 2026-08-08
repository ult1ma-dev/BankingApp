"""Тесты функций модуля masks."""

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    ("card_number", "expected"),
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("12345678901234567890", "1234 56** **** 7890"),
        ("1234", "1234 **** **12 34"),
        ("", "**** **  "),
    ],
)
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    """Проверить маскировку номеров карт разной длины."""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    ("account_number", "expected"),
    [
        ("73654108430135874305", "**4305"),
        ("00000000000000000000", "**0000"),
        ("123456789012345678901234", "**1234"),
        ("1234", "**1234"),
        ("123", "**123"),
        ("", "**"),
    ],
)
def test_get_mask_account(account_number: str, expected: str) -> None:
    """Проверить маскировку номеров счетов разной длины."""
    assert get_mask_account(account_number) == expected
