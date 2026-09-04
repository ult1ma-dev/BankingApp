import json
import logging
from json import JSONDecodeError
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_json_file(path: str | Path) -> list[dict[str, Any]]:
    """Прочитать из JSON-файла список финансовых транзакций.

    Вернуть пустой список, если файл отсутствует, пуст, содержит некорректный
    JSON или JSON верхнего уровня не является списком.
    """

    logger.debug("Начало чтения JSON-файла: %s", path)

    try:
        with open(path, "r", encoding="UTF-8") as f:
            file_as_object = json.load(f)
    except FileNotFoundError:
        logger.error("JSON-файл не найден: %s", path)
        return []
    except JSONDecodeError as error:
        logger.error("Ошибка декодирования JSON-файла %s: %s", path, error)
        return []

    if not isinstance(file_as_object, list):
        logger.error("JSON-файл %s не содержит список транзакций", path)
        return []

    logger.info("JSON-файл %s успешно прочитан, транзакций: %d", path, len(file_as_object))
    return file_as_object
