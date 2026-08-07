"""Общие фикстуры для тестов проекта."""

import pytest


@pytest.fixture
def operations() -> list[dict[str, object]]:
    """Вернуть список операций с разными статусами и датами."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def operations_with_same_date() -> list[dict[str, object]]:
    """Вернуть операции, среди которых есть одинаковые даты."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T10:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2024-03-11T10:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-12-31T23:59:59"},
    ]


@pytest.fixture
def operations_with_nonstandard_dates() -> list[dict[str, object]]:
    """Вернуть операции с нестандартными строками вместо ISO-дат."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "31.12.2023"},
        {"id": 2, "state": "EXECUTED", "date": "invalid-date"},
        {"id": 3, "state": "CANCELED", "date": ""},
    ]
