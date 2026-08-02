def filter_by_state(list_of_dicts: list[dict[str, object]], state: str = "EXECUTED") -> list[dict[str, object]]:
    filtered_dicts = []

    for operation in list_of_dicts:
        if operation["state"] == state:
            filtered_dicts.append(operation)

    return filtered_dicts
