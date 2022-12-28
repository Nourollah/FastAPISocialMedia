# This file just sample for writing test with unittest
# Created by AmirMasoud Nourollah

from app.banktest import BankAccount
import unittest
from parameterized import parameterized


class TestBankAccount(unittest.TestCase):

    def setUp(self) -> None:
        self.zero_bank_account = BankAccount()
        self.bank_account = BankAccount(100)

    def tearDown(self) -> None:
        del self.bank_account
        del self.zero_bank_account

    def test_balance(self):
        self.assertEqual(self.bank_account.balance, 100)
        self.assertEqual(self.zero_bank_account.balance, 0)

    def test_withdraw(self):
        self.bank_account.withdraw(10)
        self.assertEqual(self.bank_account.balance, 90)

    def test_deposit(self):
        self.bank_account.deposit(5)
        self.assertEqual(self.bank_account.balance, 105)

    @parameterized.expand([[15, 55, 10],
                           [7, 9, 4],
                           [10, 15, 10]])
    def test_transaction(self, deposit_amount, withdraw_amount, expected_balance):
        with self.assertRaises(ValueError):
            self.zero_bank_account.deposit(deposit_amount)
            self.zero_bank_account.withdraw(withdraw_amount)
            self.assertEqual(self.zero_bank_account.balance, expected_balance)
