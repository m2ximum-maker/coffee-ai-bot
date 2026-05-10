import unittest

from formatting import format_created_at, format_expense_item


class FormatCreatedAtTest(unittest.TestCase):
    def test_format_created_at(self) -> None:
        self.assertEqual(format_created_at("2026-05-10T02:24:00"), "10.05.2026 02:24")


class FormatExpenseItemTest(unittest.TestCase):
    def test_format_expense_item_with_coffee_shop(self) -> None:
        self.assertEqual(
            format_expense_item(1, 100, "американо", "Жирафери", "2026-05-10T02:24:00"),
            "1 | 100 ₽ | американо | Жирафери | 10.05.2026 02:24",
        )

    def test_format_expense_item_without_coffee_shop(self) -> None:
        self.assertEqual(
            format_expense_item(1, 100, "американо", None, "2026-05-10T02:24:00"),
            "1 | 100 ₽ | американо | - | 10.05.2026 02:24",
        )


if __name__ == "__main__":
    unittest.main()
