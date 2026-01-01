import unittest
import os
import json
from src.transaction_repository import TransactionRepository
from src.transaction import Transaction, TransactionType, Category, DateTime, CategoryType


class TestTransactionRepository(unittest.TestCase):

    def setUp(self):
        """
        初始化测试用例所需的示例数据
        """
        self.category1 = Category(TransactionType.EXPENSE, CategoryType.FOOD)
        self.category2 = Category(TransactionType.INCOME, CategoryType.SALARY)

        self.transactions = [
            Transaction(name="Lunch", amount=20.0, transaction_type=TransactionType.EXPENSE,
                        category=self.category1, datetime=DateTime(2023, 1, 1, 12, 0), remarks="Lunch meal"),
            Transaction(name="Dinner", amount=30.0, transaction_type=TransactionType.EXPENSE,
                        category=self.category1, datetime=DateTime(2023, 1, 2, 19, 0), remarks="Dinner meal"),
            Transaction(name="Salary", amount=3000.0, transaction_type=TransactionType.INCOME,
                        category=self.category2, datetime=DateTime(2023, 1, 5, 9, 0), remarks="Monthly salary"),
        ]
        self.repo = TransactionRepository(self.transactions)

    def test_insert(self):
        transaction = Transaction(name="Test", amount=150.0, transaction_type=TransactionType.INCOME,
                                   category=self.category2, datetime=DateTime(2023, 1, 10, 12, 0))
        initial_count = self.repo.get_count()
        self.repo.insert(transaction)
        self.assertEqual(self.repo.get_count(), initial_count + 1)
        self.assertIn(transaction, self.repo.get_all())

    def test_erase(self):
        transaction_to_remove = self.transactions[0]
        self.repo.erase(transaction_to_remove)
        self.assertNotIn(transaction_to_remove, self.repo.get_all())

    def test_filter_by_time_range(self):
        filtered_repo = self.repo.filter_by_time_range(DateTime(2023, 1, 1, 0, 0), DateTime(2023, 1, 2, 23, 59))
        self.assertEqual(filtered_repo.get_count(), 2)
        for transaction in filtered_repo.get_all():
            self.assertTrue(DateTime(2023, 1, 1, 0, 0).__lt__(transaction.datetime) and \
                            transaction.datetime.__lt__(DateTime(2023, 1, 2, 23, 59)))

    def test_filter_by_type(self):
        filtered_repo = self.repo.filter_by_type(TransactionType.EXPENSE)
        self.assertEqual(filtered_repo.get_count(), 2)
        for transaction in filtered_repo.get_all():
            self.assertEqual(transaction.transaction_type, TransactionType.EXPENSE)

    def test_filter_by_category(self):
        filtered_repo = self.repo.filter_by_category(self.category1)
        self.assertEqual(filtered_repo.get_count(), 2)
        for transaction in filtered_repo.get_all():
            self.assertEqual(transaction.category, self.category1)

    def test_sort_by_datetime(self):
        sorted_repo = self.repo.sort_by_datetime()
        transactions = sorted(self.transactions, key=lambda t: t.datetime)
        self.assertEqual(sorted_repo.get_all(), transactions)

    def test_get_total_amount(self):
        total_amount = sum(t.amount for t in self.transactions)
        self.assertEqual(self.repo.get_total_amount(), total_amount)

    def test_get_average_amount(self):
        average_amount = sum(t.amount for t in self.transactions) / len(self.transactions)
        self.assertEqual(self.repo.get_average_amount(), average_amount)

    def test_get_max_amount(self):
        max_amount = max(t.amount for t in self.transactions)
        self.assertEqual(self.repo.get_max_amount(), max_amount)

    def test_get_min_amount(self):
        min_amount = min(t.amount for t in self.transactions)
        self.assertEqual(self.repo.get_min_amount(), min_amount)

    def test_find_by_name(self):
        transaction = self.repo.find_by_name("Lunch")
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.name, "Lunch")

    def test_clear(self):
        self.repo.clear()
        self.assertEqual(self.repo.get_count(), 0)
        self.assertEqual(self.repo.get_all(), [])

    def test_save_and_load_json(self):
        file_path = "test_transactions.json"
        self.repo.save_to_json(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Verify saved data
        self.assertEqual(len(data), len(self.transactions))
        for saved_transaction, original_transaction in zip(data, self.transactions):
            self.assertEqual(saved_transaction["name"], original_transaction.name)
            self.assertEqual(saved_transaction["amount"], original_transaction.amount)
            self.assertEqual(saved_transaction["transaction_type"], original_transaction.transaction_type.value)

        # Load and verify repository
        loaded_repo = TransactionRepository.load_from_json(file_path)
        self.assertEqual(loaded_repo.get_count(), len(self.transactions))
        self.assertEqual(len(loaded_repo.get_all()), len(self.transactions))
        os.remove(file_path)  # Clean up test file


if __name__ == "__main__":
    unittest.main()
