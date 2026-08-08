import unittest
from unittest.mock import Mock

from main import BankAccount, InsufficientBalanceError, InvalidAmountError


class TestBankAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Runs ONCE, before any test in this class starts.
        print("\n[setUpClass] Starting BankAccount test suite...")

    @classmethod
    def tearDownClass(cls):
        # Runs ONCE, after all tests in this class have finished.
        print("[tearDownClass] Finished BankAccount test suite.\n")

    def setUp(self):
        # Runs before EVERY test method. Fresh accounts each time
        # so tests never leak state into one another.
        self.account_a = BankAccount("Alice", 1000)
        self.account_b = BankAccount("Bob", 500)

    def tearDown(self):
        # Runs after EVERY test method.
        # Everything is in-memory, but it is good practice to show the hook.
        del self.account_a
        del self.account_b

    # ---------- 1. Test credit ----------
    def test_credit_increases_balance(self):
        with self.subTest("credit a positive amount"):
            new_balance = self.account_a.credit(500)

            self.assertEqual(new_balance, 1500)
            self.assertEqual(self.account_a.get_balance(), 1500)

        with self.subTest("credit zero or negative should raise"):
            for bad_amount in [0, -50]:
                with self.subTest(amount=bad_amount):
                    with self.assertRaises(InvalidAmountError):
                        self.account_a.credit(bad_amount)

    # ---------- 2. Test debit ----------
    def test_debit_decreases_balance(self):
        new_balance = self.account_a.debit(200)

        self.assertEqual(new_balance, 800)
        self.assertNotEqual(new_balance, 1000)

    def test_debit_more_than_balance_raises_error(self):
        with self.assertRaises(InsufficientBalanceError):
            self.account_a.debit(5000)

    # ---------- 3. Test UPI transfer ----------
    def test_upi_transfer_between_accounts(self):
        self.account_a.upi_transfer(self.account_b, 300)

        self.assertEqual(self.account_a.get_balance(), 700)
        self.assertEqual(self.account_b.get_balance(), 800)

    def test_upi_transfer_insufficient_balance(self):
        with self.assertRaises(InsufficientBalanceError):
            self.account_a.upi_transfer(self.account_b, 10000)

    def test_upi_transfer_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.account_a.upi_transfer("not_an_account", 100)

    # ---------- 4. Test get_balance ----------
    def test_get_balance_returns_correct_value_and_type(self):
        balance = self.account_a.get_balance()

        self.assertIsInstance(balance, float)
        self.assertEqual(balance, 1000)
        self.assertGreater(balance, 0)
        self.assertLess(self.account_b.get_balance(), balance)

    # ---------- 5. Test apply_interest ----------
    def test_apply_interest_various_rates(self):
        # subTest lets us test several rate/expected-balance pairs
        # while still seeing each case reported individually on failure.
        test_cases = [
            (10, 1100.0),
            (5, 1050.0),
            (0, 1000.0),
        ]

        for rate, expected in test_cases:
            with self.subTest(rate=rate):
                account = BankAccount("TempUser", 1000)

                account.apply_interest(rate)

                # assertAlmostEqual is the right tool for float math
                self.assertAlmostEqual(
                    account.get_balance(),
                    expected,
                    places=2
                )

    def test_apply_negative_interest_raises_error(self):
        with self.assertRaises(InvalidAmountError):
            self.account_a.apply_interest(-5)

    # ---------- 6. Test get_transaction_history ----------
    def test_transaction_history_records_actions(self):
        self.account_a.credit(100)
        self.account_a.debit(50)

        history = self.account_a.get_transaction_history()

        self.assertTrue(len(history) > 0)
        self.assertFalse(len(history) == 0)

        # Check that specific keywords ended up in the log
        combined_log = " ".join(history)

        self.assertIn("Credited 100", combined_log)
        self.assertIn("Debited 50", combined_log)
        self.assertNotIn("UPI transferred", combined_log)

    # ---------- 7. Test notification sending (mocking) ----------
    def test_notification_sent_after_transfer(self):
        mock_notifier = Mock()

        sender = BankAccount(
            "Alice",
            1000,
            notifier=mock_notifier
        )

        receiver = BankAccount("Bob", 500)

        sender.upi_transfer(receiver, 200)

        mock_notifier.send_notification.assert_called_once_with(
            "200 transferred from Alice to Bob"
        )

    def test_negative_initial_balance_raises_error(self):
        with self.assertRaises(InvalidAmountError):
            BankAccount("Alice", -100)

    def test_invalid_debit_amount(self):
        for amount in [0, -50]:
            with self.subTest(amount=amount):
                with self.assertRaises(InvalidAmountError):
                    self.account_a.debit(amount)

    def test_invalid_transfer_amount(self):
        for amount in [0, -100]:
            with self.subTest(amount=amount):
                with self.assertRaises(InvalidAmountError):
                    self.account_a.upi_transfer(
                        self.account_b,
                        amount
                    )

    def test_repr(self):
        repr_str = repr(self.account_a)

        self.assertIn("Alice", repr_str)
        self.assertIn("1000", repr_str)


if __name__ == "__main__":
    unittest.main(verbosity=2)