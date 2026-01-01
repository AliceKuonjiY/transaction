import unittest
import os
from src.plot_service import PlotService
from src.transaction_repository import TransactionRepository
from src.transaction import Transaction, TransactionType, Category, DateTime, CategoryType


class TestPlotServiceIntegration(unittest.TestCase):
    def setUp(self):
        """
        准备数据文件和服务
        """
        self.file_path = "test_transactions.json"
        self.repo = TransactionRepository([
            Transaction(
                name="Lunch",
                amount=25.0,
                transaction_type=TransactionType.EXPENSE,
                category=Category(CategoryType.FOOD),
                datetime=DateTime(2023, 1, 1, 12, 0)),
            Transaction(
                name="Salary",
                amount=5000.0,
                transaction_type=TransactionType.INCOME,
                category=Category(CategoryType.SALARY),
                datetime=DateTime(2023, 1, 5, 9, 0)),
        ])
        self.repo.save_to_json(self.file_path)  # 初始化保存数据文件

    def tearDown(self):
        """
        清理测试数据
        """
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_plot_from_loaded_data(self):
        """
        测试从文件加载数据并生成图表的集成流程
        """
        # 从文件加载数据
        loaded_repo = TransactionRepository.load_from_json(self.file_path)

        # 测试生成柱状图
        bar_service = PlotService(style="bar")
        fig = bar_service.get_plot(loaded_repo)
        self.assertIsNotNone(fig, "Bar chart should be generated successfully")

        # 测试生成饼图
        pie_service = PlotService(style="pie")
        fig = pie_service.get_plot(loaded_repo)
        self.assertIsNotNone(fig, "Pie chart should be generated successfully")

    def test_full_integration_flow(self):
        """
        测试从插入数据到图表生成的完整集成流程
        """
        # 插入新数据
        new_transaction = Transaction(
            name="Dinner",
            amount=35.0,
            transaction_type=TransactionType.EXPENSE,
            category=Category(CategoryType.FOOD),
            datetime=DateTime(2023, 1, 1, 19, 0),
        )
        self.repo.insert(new_transaction)

        # 更新后生成线图
        line_service = PlotService(style="line")
        fig = line_service.get_plot(self.repo)
        self.assertIsNotNone(fig, "Line chart should reflect updated transactions")

if __name__ == "__main__":
    unittest.main()
