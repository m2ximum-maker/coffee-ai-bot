import os
import tempfile
import unittest

from db import get_expenses, init_db
from services import (
    create_expense,
    delete_user_expense,
    get_user_expenses,
    get_user_total_expenses,
)


class CreateExpenseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_file.close()
        self.previous_db_path = os.environ.get("DB_PATH")
        os.environ["DB_PATH"] = self.db_file.name
        init_db()

    def tearDown(self) -> None:
        if self.previous_db_path is None:
            os.environ.pop("DB_PATH", None)
        else:
            os.environ["DB_PATH"] = self.previous_db_path

        os.unlink(self.db_file.name)

    def test_create_expense(self) -> None:
        expense = create_expense(
            user_id=1,
            amount=100,
            drink="американо",
            coffee_shop="Жирафери",
        )

        expenses = get_expenses(user_id=1)

        self.assertEqual(expense.id, expenses[0].id)
        self.assertEqual(expense.amount, 100)
        self.assertEqual(expense.drink, "американо")
        self.assertEqual(expense.coffee_shop, "Жирафери")
        self.assertTrue(expense.created_at)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount, 100)
        self.assertEqual(expenses[0].drink, "американо")
        self.assertEqual(expenses[0].coffee_shop, "Жирафери")

    def test_get_user_expenses(self) -> None:
        create_expense(user_id=1, amount=100, drink="американо", coffee_shop=None)

        expenses = get_user_expenses(user_id=1)

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount, 100)

    def test_get_user_total_expenses(self) -> None:
        create_expense(user_id=1, amount=100, drink="американо", coffee_shop=None)
        create_expense(user_id=1, amount=250, drink="капучино", coffee_shop=None)

        self.assertEqual(get_user_total_expenses(user_id=1), 350)

    def test_delete_user_expense(self) -> None:
        create_expense(user_id=1, amount=100, drink="американо", coffee_shop=None)
        expense_id = get_user_expenses(user_id=1)[0].id

        self.assertTrue(delete_user_expense(user_id=1, expense_id=expense_id))
        self.assertEqual(get_user_expenses(user_id=1), [])


if __name__ == "__main__":
    unittest.main()
