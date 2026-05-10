from datetime import datetime

from models import Expense


def format_created_at(created_at: str) -> str:
    dt = datetime.fromisoformat(created_at)
    return dt.strftime("%d.%m.%Y %H:%M")


def format_expense_item(expense: Expense) -> str:
    coffee_shop_text = expense.coffee_shop or "-"
    created_at_text = format_created_at(expense.created_at)

    return f"{expense.id} | {expense.amount} ₽ | {expense.drink} | {coffee_shop_text} | {created_at_text}"
