from typing import Optional

ERROR_MISSING_AMOUNT = "missing amount"
ERROR_INVALID_AMOUNT = "invalid amount"
ERROR_AMOUNT_NOT_POSITIVE = "amount must be positive"
ERROR_MISSING_EXPENSE_ID = "missing expense id"
ERROR_INVALID_EXPENSE_ID = "invalid expense id"
ERROR_EXPENSE_ID_NOT_POSITIVE = "expense id must be positive"


def parse_add_command(text: str) -> tuple[int, str, Optional[str]]:
    parts = text.strip().split(maxsplit=3)

    if len(parts) < 2:
        raise ValueError(ERROR_MISSING_AMOUNT)

    amount_raw = parts[1]

    try:
        amount = int(amount_raw)
    except ValueError as error:
        raise ValueError(ERROR_INVALID_AMOUNT) from error

    if amount <= 0:
        raise ValueError(ERROR_AMOUNT_NOT_POSITIVE)

    drink = parts[2].strip() if len(parts) > 2 else "кофе"
    coffee_shop = parts[3].strip() if len(parts) > 3 else None

    return amount, drink, coffee_shop


def get_add_error_message(error: ValueError) -> str:
    error_code = str(error)

    if error_code == ERROR_MISSING_AMOUNT:
        return "Сумма отсутствует. Пример: /add 250 капучино"

    if error_code == ERROR_INVALID_AMOUNT:
        return "Не понял сумму. Пример: /add 250 капучино"

    if error_code == ERROR_AMOUNT_NOT_POSITIVE:
        return "Сумма должна быть больше нуля"

    return (
        "☕ Формат: /add <сумма> [напиток] [кофейня]\n"
        "Пример: /add 250 капучино"
    )


def parse_delete_command(text: str) -> int:
    parts = text.strip().split(maxsplit=1)

    if len(parts) < 2:
        raise ValueError(ERROR_MISSING_EXPENSE_ID)

    expense_id_raw = parts[1]

    try:
        expense_id = int(expense_id_raw)
    except ValueError as error:
        raise ValueError(ERROR_INVALID_EXPENSE_ID) from error

    if expense_id <= 0:
        raise ValueError(ERROR_EXPENSE_ID_NOT_POSITIVE)

    return expense_id


def get_delete_error_message(error: ValueError) -> str:
    error_code = str(error)

    if error_code == ERROR_MISSING_EXPENSE_ID:
        return "Укажи id записи: /delete 3"

    if error_code == ERROR_INVALID_EXPENSE_ID:
        return "Не понял id записи. Пример: /delete 3"

    if error_code == ERROR_EXPENSE_ID_NOT_POSITIVE:
        return "Id записи должен быть больше нуля"

    return "Формат: /delete <id>\nПример: /delete 3"
