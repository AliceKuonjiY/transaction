import unittest
import os
from src.transaction_repository import TransactionRepository
from src.transaction import Transaction, TransactionType, Category, DateTime, CategoryType


class TestTransactionRepositoryIntegration(unittest.TestCase):

    def setUp(self):
        """
        设置集成测试的数据和必要环境
        """
        self.category_food = Category(TransactionType.EXPENSE, CategoryType.FOOD)
        self.category_salary = Category(TransactionType.INCOME, CategoryType.SALARY)

        # 示例交易记录
        self.transactions = [
            Transaction(name="Lunch", amount=15.0, transaction_type=TransactionType.EXPENSE,
                        category=self.category_food, datetime=DateTime(2023, 10, 1, 12, 0), remarks="Lunch meal"),
            Transaction(name="Salary", amount=5000.0, transaction_type=TransactionType.INCOME,
                        category=self.category_salary, datetime=DateTime(2023, 10, 1, 9, 0), remarks="Monthly salary"),
        ]

        # 定义文件路径
        self.file_path = "test_transactions.json"

    def tearDown(self):
        """
        清理生成的测试文件，保持测试环境整洁
        """
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_save_and_load_transactions(self):
        """
        集成测试流程：插入交易记录 -> 保存到文件 -> 从文件加载 -> 验证完整性
        """
        # 初始化仓库并插入交易记录
        repo = TransactionRepository()
        for transaction in self.transactions:
            repo.insert(transaction)

        # 保存交易记录到 JSON 文件
        repo.save_to_json(self.file_path)
        self.assertTrue(os.path.exists(self.file_path))  # 验证文件已保存

        # 从 JSON 文件加载数据
        loaded_repo = TransactionRepository.load_from_json(self.file_path)

        # 验证加载后的数据是否与原始数据匹配
        self.assertEqual(loaded_repo.get_count(), len(self.transactions))  # 验证记录数一致
        for loaded_transaction, original_transaction in zip(loaded_repo.get_all(), self.transactions):
            self.assertEqual(loaded_transaction.name, original_transaction.name)
            self.assertEqual(loaded_transaction.amount, original_transaction.amount)
            self.assertEqual(loaded_transaction.transaction_type, original_transaction.transaction_type)
            self.assertEqual(loaded_transaction.remarks, original_transaction.remarks)

    def test_filter_and_sort_integration(self):
        """
        集成测试流程：插入交易记录 -> 按类别过滤 -> 按时间排序
        """
        repo = TransactionRepository(self.transactions)

        # 按交易类别过滤（仅保留收入）
        filtered_repo = repo.filter_by_type(TransactionType.INCOME)
        self.assertEqual(filtered_repo.get_count(), 1)
        self.assertEqual(filtered_repo.get_all()[0].name, "Salary")

        # 按时间排序（假设不影响记录的正确性）
        sorted_repo = repo.sort_by_datetime()
        transactions_sorted = sorted(self.transactions, key=lambda t: t.datetime)
        self.assertEqual(sorted_repo.get_all(), transactions_sorted)

    def test_end_to_end_workflow(self):
        """
        使用JSON文件模拟端到端场景工作流。
        流程：1. 创建交易 -> 2. 保存 -> 3. 加载 -> 4. 插入新交易 -> 5. 再次保存和加载
        """
        repo = TransactionRepository(self.transactions)

        # 保存初始仓库到文件
        repo.save_to_json(self.file_path)

        # 加载保存的仓库
        loaded_repo = TransactionRepository.load_from_json(self.file_path)

        # 验证加载数据与原始数据一致
        self.assertEqual(loaded_repo.get_count(), len(self.transactions))

        # 插入新交易记录
        new_transaction = Transaction(
            name="Dinner", amount=25.0, transaction_type=TransactionType.EXPENSE,
            category=self.category_food, datetime=DateTime(2023, 10, 1, 19, 0), remarks="Dinner meal"
        )
        loaded_repo.insert(new_transaction)

        # 保存更新后的数据并重新加载
        loaded_repo.save_to_json(self.file_path)
        updated_repo = TransactionRepository.load_from_json(self.file_path)

        # 验证更新是否正确
        self.assertEqual(updated_repo.get_count(), len(self.transactions) + 1)
        self.assertIsNotNone(updated_repo.find_by_name("Dinner"))


if __name__ == "__main__":
    unittest.main()
