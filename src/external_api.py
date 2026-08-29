import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """Вернуть сумму транзакции в рублях.

    Сумма в RUB возвращается без запроса. Суммы в USD и EUR конвертируются
    через Exchange Rates Data API.
    """

    operation_sum = float(transaction["operationAmount"]["amount"])
    currency_code = transaction["operationAmount"]["currency"]["code"]

    if currency_code == "RUB":
        return operation_sum

    if not API_KEY:
        raise ValueError("Не задан API-ключ EXCHANGE_RATES_API_KEY")

    response = requests.get(
        API_URL,
        params={"amount": str(operation_sum), "from": currency_code, "to": "RUB"},
        headers={"apikey": API_KEY},
    )

    response.raise_for_status()

    response_json: dict[str, Any] = response.json()

    return float(response_json["result"])
