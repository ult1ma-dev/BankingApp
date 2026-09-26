"""Тесты функций модуля processing."""

import pytest

from src.processing import filter_by_state, process_bank_operations, process_bank_search, sort_by_date


def test_filter_by_state_default(operations: list[dict[str, object]]) -> None:
    """Проверить фильтрацию со статусом EXECUTED по умолчанию."""
    result = filter_by_state(operations)

    assert [operation["id"] for operation in result] == [41428829, 939719570]
    assert result is not operations


@pytest.mark.parametrize(
    ("state", "expected_ids"),
    [
        ("EXECUTED", [41428829, 939719570]),
        ("CANCELED", [594226727, 615064591]),
        ("PENDING", []),
    ],
)
def test_filter_by_state(operations: list[dict[str, object]], state: str, expected_ids: list[int]) -> None:
    """Проверить фильтрацию для разных значений статуса."""
    result = filter_by_state(operations, state)

    assert [operation["id"] for operation in result] == expected_ids


def test_filter_by_state_empty_list() -> None:
    """Проверить фильтрацию пустого списка."""
    assert filter_by_state([]) == []


def test_filter_by_state_without_state() -> None:
    """Проверить исключение при отсутствии ключа state."""
    operations: list[dict[str, object]] = [{"id": 1, "date": "2024-03-11T10:00:00"}]

    with pytest.raises(KeyError, match="state"):
        filter_by_state(operations)


@pytest.mark.parametrize(
    ("reverse", "expected_ids"),
    [
        (True, [41428829, 615064591, 594226727, 939719570]),
        (False, [939719570, 594226727, 615064591, 41428829]),
    ],
)
def test_sort_by_date(operations: list[dict[str, object]], reverse: bool, expected_ids: list[int]) -> None:
    """Проверить сортировку дат по убыванию и возрастанию."""
    original_operations = operations.copy()

    result = sort_by_date(operations, reverse)

    assert [operation["id"] for operation in result] == expected_ids
    assert result is not operations
    assert operations == original_operations


def test_sort_by_date_default(operations: list[dict[str, object]]) -> None:
    """Проверить сортировку по убыванию по умолчанию."""
    result = sort_by_date(operations)

    assert [operation["id"] for operation in result] == [41428829, 615064591, 594226727, 939719570]


def test_sort_by_date_with_same_dates(operations_with_same_date: list[dict[str, object]]) -> None:
    """Проверить сохранение порядка операций с одинаковой датой."""
    result = sort_by_date(operations_with_same_date)

    assert [operation["id"] for operation in result] == [1, 2, 3]


@pytest.mark.parametrize(
    ("reverse", "expected_ids"),
    [
        (True, [2, 1, 3]),
        (False, [3, 1, 2]),
    ],
)
def test_sort_by_date_with_nonstandard_dates(
    operations_with_nonstandard_dates: list[dict[str, object]], reverse: bool, expected_ids: list[int]
) -> None:
    """Проверить строковую сортировку нестандартных дат."""
    result = sort_by_date(operations_with_nonstandard_dates, reverse)

    assert [operation["id"] for operation in result] == expected_ids


def test_sort_by_date_without_date() -> None:
    """Проверить исключение при отсутствии ключа date."""
    operations: list[dict[str, object]] = [{"id": 1, "state": "EXECUTED"}]

    with pytest.raises(KeyError, match="date"):
        sort_by_date(operations)


def test_sort_by_date_empty_list() -> None:
    """Проверить сортировку пустого списка."""
    assert sort_by_date([]) == []


@pytest.mark.parametrize(
    ("search", "expected_ids"),
    [
        ("организации", [939719570, 594226727]),
        ("^Перевод со счета", [142264268, 873106923]),
        ("перевод", []),
        ("Открытие вклада", []),
    ],
)
def test_process_bank_search(transactions: list[dict[str, object]], search: str, expected_ids: list[int]) -> None:
    """Проверить поиск операций по описанию и регулярному выражению."""
    result = process_bank_search(transactions, search)

    assert [transaction["id"] for transaction in result] == expected_ids


def test_process_bank_search_without_description() -> None:
    """Операция без описания не попадает в результат поиска."""
    assert process_bank_search([{"id": 1}], "Перевод") == []


@pytest.mark.parametrize(
    ("categories", "expected"),
    [
        (
            ["Перевод организации", "Перевод со счета на счет"],
            {"Перевод организации": 2, "Перевод со счета на счет": 2},
        ),
        (["Перевод с карты на карту"], {"Перевод с карты на карту": 1}),
        (["Открытие вклада"], {}),
        ([], {}),
    ],
)
def test_process_bank_operations(
    transactions: list[dict[str, object]], categories: list[str], expected: dict[str, int]
) -> None:
    """Проверить подсчёт операций по переданным категориям."""
    assert process_bank_operations(transactions, categories) == expected
