"""Тесты главного модуля программы."""

from typing import Any
from unittest.mock import patch

import pytest

import main as main_module


@pytest.fixture
def table_transactions() -> list[dict[str, Any]]:
    """Вернуть транзакции в плоском формате CSV и XLSX."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-03-11T02:26:18",
            "amount": "100.00",
            "currency_name": "руб.",
            "currency_code": "RUB",
            "from": "",
            "to": "Счет 12345678901234567890",
            "description": "Открытие вклада",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2024-02-10T12:00:00",
            "amount": "50.00",
            "currency_name": "USD",
            "currency_code": "USD",
            "from": "Visa Classic 6831982476737658",
            "to": "Счет 12345678901234567890",
            "description": "Перевод организации",
        },
    ]


def test_prepare_transactions(table_transactions: list[dict[str, Any]]) -> None:
    """Плоская транзакция преобразуется в структуру JSON."""
    incomplete_transaction = {
        "state": "EXECUTED",
        "date": "",
        "description": "Перевод организации",
        "to": "Счет 12345678901234567890",
    }

    result = main_module.prepare_transactions([{}, incomplete_transaction, *table_transactions])

    assert len(result) == 2
    assert result[0]["operationAmount"] == {
        "amount": "100.00",
        "currency": {"name": "руб.", "code": "RUB"},
    }
    assert "operationAmount" not in table_transactions[0]


def test_main_with_json(transactions: list[dict[str, Any]], capsys: pytest.CaptureFixture[str]) -> None:
    """Проверить полный сценарий обработки JSON-файла."""
    answers = ["1", "executed", "да", "по убыванию", "нет", "да", "организации"]

    with patch("builtins.input", side_effect=answers), patch(
        "main.read_json_file", return_value=[{}, *transactions]
    ) as reader_mock:
        main_module.main()

    output = capsys.readouterr().out
    reader_mock.assert_called_once_with("data/operations.json")
    assert "Для обработки выбран JSON-файл." in output
    assert "Всего банковских операций в выборке: 1" in output
    assert "30.06.2018 Перевод организации" in output
    assert "Счет **6952 -> Счет **6702" in output
    assert "Сумма: 9824.07 USD" in output


def test_main_with_csv(table_transactions: list[dict[str, Any]], capsys: pytest.CaptureFixture[str]) -> None:
    """Проверить рублёвую фильтрацию данных из CSV."""
    answers = ["2", "EXECUTED", "нет", "да", "нет"]

    with patch("builtins.input", side_effect=answers), patch(
        "main.read_transactions_from_csv", return_value=table_transactions
    ) as reader_mock:
        main_module.main()

    output = capsys.readouterr().out
    reader_mock.assert_called_once_with("data/transactions.csv")
    assert "Для обработки выбран CSV-файл." in output
    assert "Всего банковских операций в выборке: 1" in output
    assert "11.03.2024 Открытие вклада" in output
    assert "Счет **7890" in output
    assert "Сумма: 100.00 руб." in output


def test_main_with_excel_without_results(
    table_transactions: list[dict[str, Any]], capsys: pytest.CaptureFixture[str]
) -> None:
    """Проверить сообщение при отсутствии подходящих XLSX-транзакций."""
    answers = ["3", "PENDING", "нет", "нет", "нет"]

    with patch("builtins.input", side_effect=answers), patch(
        "main.read_transactions_from_excel", return_value=table_transactions
    ) as reader_mock:
        main_module.main()

    output = capsys.readouterr().out
    reader_mock.assert_called_once_with("data/transactions_excel.xlsx")
    assert "Для обработки выбран Excel-файл." in output
    assert "Не найдено ни одной транзакции" in output


def test_main_with_invalid_menu_item(capsys: pytest.CaptureFixture[str]) -> None:
    """При неизвестном пункте меню программа корректно завершается."""
    with patch("builtins.input", return_value="9"):
        main_module.main()

    assert "Неверный пункт меню." in capsys.readouterr().out


def test_ask_status_repeats_after_wrong_answer(capsys: pytest.CaptureFixture[str]) -> None:
    """Статус запрашивается повторно после неправильного ответа."""
    with patch("builtins.input", side_effect=["unknown", " executed "]):
        result = main_module.ask_status()

    assert result == "EXECUTED"
    assert "Статус операции UNKNOWN недоступен." in capsys.readouterr().out


def test_ask_yes_no_repeats_after_wrong_answer(capsys: pytest.CaptureFixture[str]) -> None:
    """Ответ «да» или «нет» запрашивается до корректного ввода."""
    with patch("builtins.input", side_effect=["не знаю", " ДА "]):
        result = main_module.ask_yes_no("Продолжить?")

    assert result is True
    assert "Введите 'да' или 'нет'" in capsys.readouterr().out


def test_ask_sort_order_repeats_after_wrong_answer(capsys: pytest.CaptureFixture[str]) -> None:
    """Порядок сортировки запрашивается до корректного ввода."""
    with patch("builtins.input", side_effect=["не знаю", "по возрастанию"]):
        result = main_module.ask_sort_order()

    assert result is False
    assert "Введите 'по возрастанию' или 'по убыванию'" in capsys.readouterr().out
