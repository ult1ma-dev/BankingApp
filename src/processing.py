def filter_by_state(list_of_dicts: list, state = 'EXECUTED') -> list:
    filtered_dicts = []
    for dict in list_of_dicts:
        if dict['state'] == state:
            filtered_dicts.append(dict)