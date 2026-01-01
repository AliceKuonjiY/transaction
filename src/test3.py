import unittest
from src.plot_service import PlotService
from src.transaction_repository import TransactionRepository
from src.transaction import Transaction, TransactionType, Category, DateTime, CategoryType

class TestPlotService(unittest.TestCase):
    def setUp(self):
        """
        初始化基础交易数据和 PlotService 的实例
        """
        self.repo = TransactionRepository([
            Transaction(
                name="Lunch",
                amount=20.0,
                transaction_type=TransactionType.EXPENSE,
                category=Category(CategoryType.FOOD),
                datetime=DateTime(2023, 1, 1, 12, 0)),
            Transaction(
                name="Dinner",
                amount=40.0,
                transaction_type=TransactionType.EXPENSE,
                category=Category(CategoryType.FOOD),
                datetime=DateTime(2023, 1, 1, 19, 0)),
            Transaction(
                name="Salary",
                amount=3000.0,
                transaction_type=TransactionType.INCOME,
                category=Category(CategoryType.SALARY),
                datetime=DateTime(2023, 1, 5, 9, 0)),
        ])
        self.bar_service = PlotService(style="bar")
        self.line_service = PlotService(style="line")
        self.pie_service = PlotService(style="pie")

    def test_bar_plot(self):
        """
        测试柱状图生成
        """
        fig = self.bar_service.get_plot(self.repo)
        self.assertIsNotNone(fig, "Bar plot should generate a figure")
        self.assertEqual(len(fig.axes), 1, "Expected one axis for bar plot")
        ax = fig.axes[0]
        self.assertEqual(len(ax.patches), 2, "Bar plot should have 2 bars (categories)")

    def test_line_plot(self):
        """
        测试折线图生成
        """
        fig = self.line_service.get_plot(self.repo)
        self.assertIsNotNone(fig, "Line plot should generate a figure")
        self.assertEqual(len(fig.axes), 1, "Expected one axis for line plot")
        ax = fig.axes[0]
        self.assertEqual(len(ax.lines), 1, "Line plot should have one line")
        self.assertGreater(len(ax.get_xticks()), 0, "Line plot should have labeled ticks")

    def test_pie_chart(self):
        """
        测试饼图生成
        """
        fig = self.pie_service.get_plot(self.repo)
        self.assertIsNotNone(fig, "Pie chart should generate a figure")
        self.assertEqual(len(fig.axes), 1, "Expected one axis for pie chart")
        ax = fig.axes[0]
        self.assertEqual(len(ax.patches), 2, "Pie chart should have 2 slices (categories)")

    def test_unsupported_plot_style(self):
        """
        测试不支持的图表样式
        """
        with self.assertRaises(ValueError):
            unsupported_service = PlotService(style="scatter")
            unsupported_service.get_plot(self.repo)

if __name__ == "__main__":
    unittest.main()
