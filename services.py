from typing import Optional

from db import add_expense, delete_expense, get_expenses, get_total_expenses
from models import Expense


def create_expense(
    user_id: int,
    amount: int,
    drink: str,
    coffee_shop: Optional[str],
) -> Expense:
    return add_expense(
        user_id=user_id,
        amount=amount,
        drink=drink,
        coffee_shop=coffee_shop,
    )


def delete_user_expense(user_id: int, expense_id: int) -> bool:
    return delete_expense(
        user_id=user_id,
        expense_id=expense_id,
    )


def get_user_expenses(user_id: int) -> list[Expense]:
    return get_expenses(user_id=user_id)


def get_user_total_expenses(user_id: int) -> int:
    return get_total_expenses(user_id=user_id)
