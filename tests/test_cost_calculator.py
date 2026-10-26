import unittest

from task1_models_tokens_cost.cost_calculator import calculate_cost


class CostCalculatorTests(unittest.TestCase):
    def test_calculates_input_and_output_cost(self):
        self.assertAlmostEqual(calculate_cost(1_000_000, 2_000_000, 0.5, 1.5), 3.5)

    def test_zero_tokens_cost_nothing(self):
        self.assertEqual(calculate_cost(0, 0, 0.5, 1.5), 0)

    def test_rejects_negative_values(self):
        with self.assertRaises(ValueError):
            calculate_cost(-1, 0, 0.5, 1.5)


if __name__ == "__main__":
    unittest.main()
