from datetime import datetime
from typing import Optional


def format_created_at(created_at: str) -> str:
    dt = datetime.fromisoformat(created_at)
    return dt.strftime("%d.%m.%Y %H:%M")


def format_expense_item(
    index: int,
    amount: int,
    drink: str,
    coffee_shop: Optional[str],
    created_at: str,
) -> str:
    coffee_shop_text = coffee_shop or "-"
    created_at_text = format_created_at(created_at)

    return f"{index} | {amount} ₽ | {drink} | {coffee_shop_text} | {created_at_text}"
