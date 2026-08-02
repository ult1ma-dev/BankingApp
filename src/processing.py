def filter_by_state(list_of_dicts: list[dict[str, object]], state: str = "EXECUTED") -> list[dict[str, object]]:
    """Вернуть новый список словарей с указанным статусом."""

    return [operation for operation in list_of_dicts if operation["state"] == state]


def sort_by_date(list_of_dicts: list[dict[str, object]], reverse: bool = True) -> list[dict[str, object]]:
    """Вернуть новый список словарей, отсортированный по дате."""

    return sorted(list_of_dicts, key=lambda operation: str(operation["date"]), reverse=reverse)
