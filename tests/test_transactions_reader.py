"""Тесты функций модуля transactions_reader."""

from typing import Any
from unittest.mock import Mock, mock_open, patch

import pytest

from src.transactions_reader import read_transactions_from_csv, read_transactions_from_excel


@pytest.fixture
def transaction_records() -> list[dict[str, Any]]:
    """Вернуть тестовый список финансовых операций."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "amount": 100.0,
            "currency_code": "RUB",
        },
        {
            "id": 2,
            "state": "CANCELED",
            "amount": 50.0,
            "currency_code": "USD",
        },
    ]


def test_read_transactions_from_csv(transaction_records: list[dict[str, Any]]) -> None:
    """Функция читает CSV и возвращает список словарей."""
    file_mock = mock_open()
    dict_reader_mock = Mock(return_value=transaction_records)

    with patch("src.transactions_reader.open", file_mock), patch(
        "src.transactions_reader.csv.DictReader", dict_reader_mock
    ):
        result = read_transactions_from_csv("data/transactions.csv")

    file_mock.assert_called_once_with("data/transactions.csv", encoding="utf-8")
    opened_file = file_mock.return_value.__enter__.return_value
    dict_reader_mock.assert_called_once_with(opened_file, delimiter=";")
    assert result == transaction_records
    assert isinstance(result, list)
    assert all(isinstance(transaction, dict) for transaction in result)


def test_read_transactions_from_empty_csv() -> None:
    """Для CSV без операций функция возвращает пустой список."""
    file_mock = mock_open(read_data="id,state,date\n")

    with patch("src.transactions_reader.open", file_mock):
        result = read_transactions_from_csv("empty.csv")

    assert result == []


def test_read_transactions_from_excel(transaction_records: list[dict[str, Any]]) -> None:
    """Функция читает Excel и возвращает список словарей."""
    dataframe_mock = Mock()
    dataframe_mock.to_dict.return_value = transaction_records

    with patch("src.transactions_reader.pd.read_excel", return_value=dataframe_mock) as read_excel_mock:
        result = read_transactions_from_excel("data/transactions_excel.xlsx")

    read_excel_mock.assert_called_once_with("data/transactions_excel.xlsx")
    dataframe_mock.to_dict.assert_called_once_with(orient="records")
    assert result == transaction_records
    assert isinstance(result, list)
    assert all(isinstance(transaction, dict) for transaction in result)


def test_read_transactions_from_empty_excel() -> None:
    """Для Excel без операций функция возвращает пустой список."""
    dataframe_mock = Mock()
    dataframe_mock.to_dict.return_value = []

    with patch("src.transactions_reader.pd.read_excel", return_value=dataframe_mock):
        result = read_transactions_from_excel("empty.xlsx")

    dataframe_mock.to_dict.assert_called_once_with(orient="records")
    assert result == []
