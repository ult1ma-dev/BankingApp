def filter_by_state(list_of_dicts: list[dict[str, object]], state: str = "EXECUTED") -> list[dict[str, object]]:
    filtered_dicts = []

    for operation in list_of_dicts:
        if operation["state"] == state:
            filtered_dicts.append(operation)

    return filtered_dicts


def sort_by_date(list_of_dicts: list[dict[str, object]], reverse: bool = True) -> list[dict[str, object]]:
    sorted_dicts = sorted(
        list_of_dicts,
        key=lambda operation: str(operation["date"]),
        reverse=reverse,
    )
    return sorted_dicts