import os
import tempfile
import unittest

from db import add_expense, delete_expense, get_expenses, init_db


class DeleteExpenseTest(unittest.TestCase):
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

    def test_delete_own_expense(self) -> None:
        add_expense(user_id=1, amount=100, drink="американо")
        expense_id = get_expenses(user_id=1)[0][0]

        self.assertTrue(delete_expense(user_id=1, expense_id=expense_id))
        self.assertEqual(get_expenses(user_id=1), [])

    def test_cannot_delete_another_user_expense(self) -> None:
        add_expense(user_id=1, amount=100, drink="американо")
        expense_id = get_expenses(user_id=1)[0][0]

        self.assertFalse(delete_expense(user_id=2, expense_id=expense_id))
        self.assertEqual(len(get_expenses(user_id=1)), 1)


if __name__ == "__main__":
    unittest.main()
