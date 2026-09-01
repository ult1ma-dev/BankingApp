import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any


def read_json_file(path: str | Path) -> list[dict[str, Any]]:
    """Прочитать из JSON-файла список финансовых транзакций.

    Вернуть пустой список, если файл отсутствует, пуст, содержит некорректный
    JSON или JSON верхнего уровня не является списком.
    """

    try:
        with open(path, "r", encoding="UTF-8") as f:
            file_as_object = json.load(f)

        if isinstance(file_as_object, list):
            return file_as_object

        return []

    except (FileNotFoundError, JSONDecodeError):
        return []
