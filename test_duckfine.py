import unittest

from duckfine import DuckFine


class TestDuckFineInit(unittest.TestCase):

    def test_stores_member_id(self):
        fine = DuckFine("M001")
        self.assertEqual(fine.member_id, "M001")

    def test_total_owed_starts_at_zero(self):
        fine = DuckFine("M001")
        self.assertEqual(fine.total_owed, 0.0)


class TestDuckFineCharge(unittest.TestCase):

    def setUp(self):
        self.fine = DuckFine("M001")

    # --- grace period ---

    def test_on_time_return_is_free(self):
        self.assertEqual(self.fine.charge(0), 0.0)

    def test_one_day_late_is_within_grace(self):
        self.assertEqual(self.fine.charge(1), 0.0)

    def test_last_grace_day_is_free(self):
        self.assertEqual(self.fine.charge(2), 0.0)

    # --- standard fee ---

    def test_first_day_after_grace_is_charged_one_daily_fee(self):
        self.assertAlmostEqual(self.fine.charge(3), 0.50)

    def test_fee_is_daily_fee_times_chargeable_days(self):
        self.assertAlmostEqual(self.fine.charge(5), 1.50)

    # --- cap ---

    def test_fee_exactly_at_cap_is_not_reduced(self):
        # 12 days late -> 10 chargeable days -> $5.00
        self.assertAlmostEqual(self.fine.charge(12), 5.00)

    def test_fee_above_cap_is_capped(self):
        self.assertAlmostEqual(self.fine.charge(30), 5.00)

    # --- deluxe ---

    def test_deluxe_doubles_fee(self):
        self.assertAlmostEqual(self.fine.charge(5, deluxe=True), 3.00)

    def test_deluxe_within_grace_is_free(self):
        self.assertEqual(self.fine.charge(2, deluxe=True), 0.0)

    def test_deluxe_fee_exactly_at_cap_is_not_reduced(self):
        # 7 days late -> 5 chargeable days -> $2.50 x 2 = $5.00
        self.assertAlmostEqual(self.fine.charge(7, deluxe=True), 5.00)

    def test_deluxe_fee_above_cap_is_capped(self):
        self.assertAlmostEqual(self.fine.charge(10, deluxe=True), 5.00)

    # --- invalid input ---

    def test_negative_days_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.fine.charge(-1)

    def test_negative_days_does_not_change_total_owed(self):
        with self.assertRaises(ValueError):
            self.fine.charge(-1)
        self.assertEqual(self.fine.total_owed, 0.0)

    # --- running total ---

    def test_charge_adds_fee_to_total_owed(self):
        fee = self.fine.charge(5)
        self.assertAlmostEqual(self.fine.total_owed, fee)

    def test_total_owed_accumulates_across_charges(self):
        self.fine.charge(5)             # 1.50
        self.fine.charge(4)             # 1.00
        self.fine.charge(4, deluxe=True)  # 2.00
        self.assertAlmostEqual(self.fine.total_owed, 4.50)

    def test_cap_applies_per_fine_not_to_total(self):
        self.fine.charge(30)
        self.fine.charge(30)
        self.assertAlmostEqual(self.fine.total_owed, 10.00)

    def test_free_charge_leaves_total_unchanged(self):
        self.fine.charge(5)
        self.fine.charge(1)
        self.assertAlmostEqual(self.fine.total_owed, 1.50)


if __name__ == "__main__":
    unittest.main()
