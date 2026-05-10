import unittest

from parsing import (
    ERROR_AMOUNT_NOT_POSITIVE,
    ERROR_INVALID_AMOUNT,
    ERROR_MISSING_AMOUNT,
    get_add_error_message,
    parse_add_command,
)


class ParseAddCommandTest(unittest.TestCase):
    def test_parse_amount_only(self) -> None:
        self.assertEqual(parse_add_command("/add 250"), (250, "кофе", None))

    def test_parse_amount_and_drink(self) -> None:
        self.assertEqual(parse_add_command("/add 250 капучино"), (250, "капучино", None))

    def test_parse_amount_drink_and_coffee_shop(self) -> None:
        self.assertEqual(
            parse_add_command("/add 250 капучино Surf Coffee"),
            (250, "капучино", "Surf Coffee"),
        )

    def test_parse_missing_amount(self) -> None:
        with self.assertRaisesRegex(ValueError, ERROR_MISSING_AMOUNT):
            parse_add_command("/add")

    def test_parse_invalid_amount(self) -> None:
        with self.assertRaisesRegex(ValueError, ERROR_INVALID_AMOUNT):
            parse_add_command("/add abc")

    def test_parse_negative_amount(self) -> None:
        with self.assertRaisesRegex(ValueError, ERROR_AMOUNT_NOT_POSITIVE):
            parse_add_command("/add -10")


class GetAddErrorMessageTest(unittest.TestCase):
    def test_missing_amount_message(self) -> None:
        self.assertEqual(
            get_add_error_message(ValueError(ERROR_MISSING_AMOUNT)),
            "Сумма отсутствует. Пример: /add 250 капучино",
        )

    def test_invalid_amount_message(self) -> None:
        self.assertEqual(
            get_add_error_message(ValueError(ERROR_INVALID_AMOUNT)),
            "Не понял сумму. Пример: /add 250 капучино",
        )

    def test_positive_amount_message(self) -> None:
        self.assertEqual(
            get_add_error_message(ValueError(ERROR_AMOUNT_NOT_POSITIVE)),
            "Сумма должна быть больше нуля",
        )


if __name__ == "__main__":
    unittest.main()
