import unittest

from formatting import format_created_at, format_expense_item
from models import Expense


class FormatCreatedAtTest(unittest.TestCase):
    def test_format_created_at(self) -> None:
        self.assertEqual(format_created_at("2026-05-10T02:24:00"), "10.05.2026 02:24")


class FormatExpenseItemTest(unittest.TestCase):
    def test_format_expense_item_with_coffee_shop(self) -> None:
        self.assertEqual(
            format_expense_item(
                Expense(
                    id=1,
                    user_id=10,
                    amount=100,
                    drink="американо",
                    coffee_shop="Жирафери",
                    created_at="2026-05-10T02:24:00",
                )
            ),
            "1 | 100 ₽ | американо | Жирафери | 10.05.2026 02:24",
        )

    def test_format_expense_item_without_coffee_shop(self) -> None:
        self.assertEqual(
            format_expense_item(
                Expense(
                    id=1,
                    user_id=10,
                    amount=100,
                    drink="американо",
                    coffee_shop=None,
                    created_at="2026-05-10T02:24:00",
                )
            ),
            "1 | 100 ₽ | американо | - | 10.05.2026 02:24",
        )


if __name__ == "__main__":
    unittest.main()
