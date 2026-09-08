import csv
from pathlib import Path
from typing import Any, cast

import pandas as pd


def read_transactions_from_csv(file_path: str | Path) -> list[dict[str, Any]]:
    """Прочитать финансовые операции из CSV-файла."""
    with open(file_path, encoding="utf-8") as file:
        transactions: list[dict[str, Any]] = list(csv.DictReader(file, delimiter=";"))
        return transactions


def read_transactions_from_excel(file_path: str | Path) -> list[dict[str, Any]]:
    """Прочитать финансовые операции из Excel-файла."""
    dataframe = pd.read_excel(file_path)
    transactions = cast(list[dict[str, Any]], dataframe.to_dict(orient="records"))
    return transactions
