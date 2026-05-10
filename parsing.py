from typing import Optional


def parse_add_command(text: str) -> tuple[int, str, Optional[str]]:
    parts = text.strip().split(maxsplit=3)

    if len(parts) < 2:
        raise ValueError("missing amount")

    amount_raw = parts[1]

    try:
        amount = int(amount_raw)
    except ValueError as error:
        raise ValueError("invalid amount") from error

    if amount <= 0:
        raise ValueError("amount must be positive")

    drink = parts[2].strip() if len(parts) > 2 else "кофе"
    coffee_shop = parts[3].strip() if len(parts) > 3 else None

    return amount, drink, coffee_shop


def get_add_error_message(error: ValueError) -> str:
    error_code = str(error)

    if error_code == "missing amount":
        return "Сумма отсутствует. Пример: /add 250 капучино"

    if error_code == "invalid amount":
        return "Не понял сумму. Пример: /add 250 капучино"

    if error_code == "amount must be positive":
        return "Сумма должна быть больше нуля"

    return (
        "☕ Формат: /add <сумма> [напиток] [кофейня]\n"
        "Пример: /add 250 капучино"
    )
