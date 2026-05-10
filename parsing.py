from typing import Optional

ERROR_MISSING_AMOUNT = "missing amount"
ERROR_INVALID_AMOUNT = "invalid amount"
ERROR_AMOUNT_NOT_POSITIVE = "amount must be positive"


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
