import csv

import pandas as pd


def read_transactions_from_csv(file_path) -> list[dict]:
    """Прочитать финансовые операции из CSV-файла."""
    with open(file_path, encoding="utf-8") as file:
        return list(csv.DictReader(file, delimiter=";"))


def read_transactions_from_excel(file_path):
    """Прочитать финансовые операции из Excel-файла."""
    dataframe = pd.read_excel(file_path)
    return dataframe.to_dict(orient="records")
