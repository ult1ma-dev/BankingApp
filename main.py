"""Точка входа в программу работы с банковскими транзакциями."""

import math
from typing import Any

from src.generators import filter_by_currency
from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.transactions_reader import read_transactions_from_csv, read_transactions_from_excel
from src.utils import read_json_file
from src.widget import get_date, mask_account_card

Transaction = dict[str, Any]


def has_value(value: object) -> bool:
    """Проверить, что значение не пустое и не является NaN."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, float):
        return not math.isnan(value)
    return True


def has_valid_operation_amount(transaction: Transaction) -> bool:
    """Проверить наличие суммы и информации о валюте."""
    operation_amount = transaction.get("operationAmount")
    if not isinstance(operation_amount, dict):
        return False

    currency = operation_amount.get("currency")
    if not isinstance(currency, dict):
        return False

    return (
        has_value(operation_amount.get("amount"))
        and has_value(currency.get("name"))
        and has_value(currency.get("code"))
    )


def load_transactions(choice: str) -> list[Transaction] | None:
    """Загрузить транзакции из выбранного пользователем файла."""
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        return read_json_file("data/operations.json")
    if choice == "2":
        print("Для обработки выбран CSV-файл.")
        return read_transactions_from_csv("data/transactions.csv")
    if choice == "3":
        print("Для обработки выбран Excel-файл.")
        return read_transactions_from_excel("data/transactions_excel.xlsx")

    print("Неверный пункт меню.")
    return None


def prepare_transactions(transactions: list[Transaction]) -> list[Transaction]:
    """Подготовить транзакции из разных файлов к общей обработке."""
    prepared_transactions: list[Transaction] = []
    required_fields = {"state", "date", "description", "to"}

    for transaction in transactions:
        if not required_fields.issubset(transaction):
            continue
        if not all(has_value(transaction[field]) for field in required_fields):
            continue

        prepared_transaction = transaction.copy()

        if "operationAmount" not in prepared_transaction:
            table_fields = {"amount", "currency_name", "currency_code"}
            if not table_fields.issubset(prepared_transaction):
                continue
            if not all(has_value(prepared_transaction[field]) for field in table_fields):
                continue

            prepared_transaction["operationAmount"] = {
                "amount": prepared_transaction["amount"],
                "currency": {
                    "name": prepared_transaction["currency_name"],
                    "code": prepared_transaction["currency_code"],
                },
            }

        if not has_valid_operation_amount(prepared_transaction):
            continue

        prepared_transactions.append(prepared_transaction)

    return prepared_transactions


def ask_status() -> str:
    """Запросить у пользователя доступный статус операции."""
    available_states = ["EXECUTED", "CANCELED", "PENDING"]
    print(
        "Введите статус, по которому необходимо выполнить фильтрацию. "
        "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
    )

    while True:
        status = input("Впишите статус: ").strip().upper()
        if status in available_states:
            return status
        print(f"Статус операции {status} недоступен.")


def ask_yes_no(question: str) -> bool:
    """Задать вопрос и получить ответ "да" или "нет"."""
    print(question)

    while True:
        answer = input("Введите 'да' или 'нет': ").strip().lower()
        if answer == "да":
            return True
        if answer == "нет":
            return False
        print("Введите 'да' или 'нет'")


def ask_sort_order() -> bool:
    """Запросить порядок сортировки и вернуть значение reverse."""
    print("По возрастанию или по убыванию?")

    while True:
        answer = input("Введите 'по возрастанию' или 'по убыванию': ").strip().lower()
        if answer == "по возрастанию":
            return False
        if answer == "по убыванию":
            return True
        print("Введите 'по возрастанию' или 'по убыванию'")


def get_masked_details(details: object) -> str:
    """Замаскировать реквизиты или вернуть пустую строку, если их нет."""
    if isinstance(details, str) and details.strip():
        return mask_account_card(details)
    return ""


def print_transaction(transaction: Transaction) -> None:
    """Напечатать одну банковскую операцию в понятном виде."""
    date = get_date(str(transaction["date"]))
    description = str(transaction["description"])
    print(f"\n{date} {description}")

    sender = get_masked_details(transaction.get("from"))
    recipient = get_masked_details(transaction.get("to"))

    if sender:
        print(f"{sender} -> {recipient}")
    elif recipient:
        print(recipient)

    operation_amount = transaction["operationAmount"]
    amount = operation_amount["amount"]
    currency_name = operation_amount["currency"]["name"]
    print(f"Сумма: {amount} {currency_name}")


def print_transactions(transactions: list[Transaction]) -> None:
    """Напечатать количество операций и каждую найденную операцию."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for transaction in transactions:
        print_transaction(transaction)


def main() -> None:
    """Запустить диалог обработки банковских транзакций."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("1. Получить информацию из JSON-файла")
    print("2. Получить информацию из CSV-файла")
    print("3. Получить информацию из XLSX-файла")

    choice = input("Выберите пункт меню: ").strip()
    transactions = load_transactions(choice)
    if transactions is None:
        return

    prepared_transactions = prepare_transactions(transactions)
    status = ask_status()
    filtered_transactions = filter_by_state(prepared_transactions, status)
    print(f"Операции отфильтрованы по статусу {status}")

    if ask_yes_no("Отсортировать операции по дате? Да/Нет"):
        reverse = ask_sort_order()
        filtered_transactions = sort_by_date(filtered_transactions, reverse=reverse)
    else:
        print("Хорошо, двигаемся дальше")

    if ask_yes_no("Выводить только рублевые транзакции? Да/Нет"):
        filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))
    else:
        print("Хорошо, двигаемся дальше")

    if ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет"):
        search = input("Введите информацию для фильтра (поиск чувствителен к регистру): ")
        filtered_transactions = process_bank_search(filtered_transactions, search)
    else:
        print("Хорошо, двигаемся дальше")

    print("Распечатываю итоговый список транзакций...")
    print_transactions(filtered_transactions)


if __name__ == "__main__":
    main()
