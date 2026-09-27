import unittest

from app import calculate_converted_amount, validate_amount


class CurrencyConverterTests(unittest.TestCase):
    def test_validate_amount_valid(self):
        amount, error = validate_amount("125.5")
        self.assertEqual(amount, 125.5)
        self.assertIsNone(error)

    def test_validate_amount_blank(self):
        amount, error = validate_amount("   ")
        self.assertIsNone(amount)
        self.assertIn("Please enter an amount", error)

    def test_validate_amount_negative(self):
        amount, error = validate_amount("-10")
        self.assertIsNone(amount)
        self.assertIn("cannot be negative", error)

    def test_validate_amount_invalid_number(self):
        amount, error = validate_amount("abc")
        self.assertIsNone(amount)
        self.assertIn("valid number", error)

    def test_calculate_converted_amount(self):
        converted = calculate_converted_amount(100, 1.25)
        self.assertAlmostEqual(converted, 125.0)


if __name__ == "__main__":
    unittest.main()
