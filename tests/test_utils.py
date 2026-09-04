import json
from pathlib import Path
from unittest.mock import mock_open, patch

from src.utils import read_json_file


def test_read_json_file() -> None:
    data = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 587085106,
            "state": "EXECUTED",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431",
        },
    ]

    with (
        patch("src.utils.open", mock_open(read_data=json.dumps(data))),
        patch("src.utils.logger.info") as mocked_info,
    ):
        result = read_json_file("data/operations.json")

    assert result == data
    mocked_info.assert_called_once()


def test_read_json_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.json"

    with patch("src.utils.logger.error") as mocked_error:
        result = read_json_file(missing_file)

    assert result == []
    mocked_error.assert_called_once()


def test_read_json_file_empty(tmp_path: Path) -> None:
    empty_file = tmp_path / "empty.json"
    empty_file.write_text("", encoding="utf-8")
    with patch("src.utils.logger.error") as mocked_error:
        result = read_json_file(empty_file)

    assert result == []
    mocked_error.assert_called_once()


def test_read_json_file_wrong_type(tmp_path: Path) -> None:
    wrong_type = tmp_path / "wrong_type.json"
    wrong_type.write_text(json.dumps({"key": "value"}), encoding="utf-8")
    with patch("src.utils.logger.error") as mocked_error:
        result = read_json_file(wrong_type)

    assert result == []
    mocked_error.assert_called_once()
