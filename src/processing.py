import re
from collections import Counter
from typing import Any


def filter_by_state(list_of_dicts: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Вернуть новый список словарей с указанным статусом."""

    return [operation for operation in list_of_dicts if operation["state"] == state]


def sort_by_date(list_of_dicts: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Вернуть новый список словарей, отсортированный по дате."""

    return sorted(list_of_dicts, key=lambda operation: str(operation["date"]), reverse=reverse)


def process_bank_search(list_of_dicts: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """Вернуть операции, в описании которых найдено заданное выражение."""

    new_operations: list[dict[str, Any]] = []
    for operation in list_of_dicts:
        description = str(operation.get("description", ""))
        result = re.search(search, description)
        if result:
            new_operations.append(operation)
    return new_operations


def process_bank_operations(data: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """Подсчитать количество операций для переданных категорий."""

    descriptions: list[str] = []
    for operation in data:
        description = str(operation.get("description", ""))
        if description in categories:
            descriptions.append(description)
    return dict(Counter(descriptions))
