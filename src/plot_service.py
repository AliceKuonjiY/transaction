"""
图表服务模块
"""

from matplotlib import pyplot as plt
from src.transaction_repository import TransactionRepository


class PlotService:
    """
    图表服务类，生成不同类型的图表
    """
    def __init__(
            self,
            style: str = "bar",
            font_size: int = 12):
        """
        初始化图表服务对象
        @param style: 图表样式，支持"bar"、"line"、"pie"
        @param font_size: 字体大小
        """
        self.style = style
        self.font_size = font_size

    def get_plot(self, transactions: TransactionRepository) -> plt.Figure:
        """
        根据交易记录生成图表
        @param transactions: 交易记录仓库
        @return: matplotlib图表对象
        """
        if self.style == "bar":
            return self._create_bar_plot(transactions)
        elif self.style == "line":
            return self._create_line_plot(transactions)
        elif self.style == "pie":
            return self._create_pie_chart(transactions)
        else:
            raise ValueError(f"Unknown plot style: {self.style}")

    def _create_bar_plot(self, transactions: TransactionRepository) -> plt.Figure:
        """
        根据交易记录生成柱状图
        @param transactions: 交易记录仓库
        @return: matplotlib图表对象
        """
        category_sums = {}
        for t in transactions.get_all():
            cat_name = t.category.name
            category_sums[cat_name] = category_sums.get(cat_name, 0) + t.amount

        fig, ax = plt.subplots()
        ax.bar(category_sums.keys(), category_sums.values())
        ax.set_title("Transaction Amounts by Category", fontsize=self.font_size)
        ax.set_xlabel("Category", fontsize=self.font_size)
        ax.set_ylabel("Total Amount", fontsize=self.font_size)
        return fig

    def _create_line_plot(self, transactions: TransactionRepository) -> plt.Figure:
        """
        根据交易记录生成折线图
        @param transactions: 交易记录仓库
        @return: matplotlib图表对象
        """
        transactions_sorted = transactions.sort_by_datetime()
        dates = []
        amounts = []
        for t in transactions_sorted.get_all():
            if t == transactions_sorted.get_all()[0]:
                dates.append(f"{t.datetime.year:04}-{t.datetime.month:02}-{t.datetime.day:02}")
                amounts.append(t.amount)
            else:
                last_date = dates[-1]
                current_date = f"{t.datetime.year:04}-{t.datetime.month:02}-{t.datetime.day:02}"
                if current_date == last_date:
                    amounts[-1] += t.amount
                else:
                    dates.append(current_date)
                    amounts.append(t.amount)

        fig, ax = plt.subplots()
        ax.plot(dates, amounts, marker='o')
        ax.set_title("Transaction Amounts Over Time", fontsize=self.font_size)
        ax.set_xlabel("Date", fontsize=self.font_size)
        ax.set_ylabel("Amount", fontsize=self.font_size)
        plt.xticks(rotation=45)
        return fig

    def _create_pie_chart(self, transactions: TransactionRepository) -> plt.Figure:
        """
        根据交易记录生成饼图
        @param transactions: 交易记录仓库
        @return: matplotlib图表对象
        """
        category_sums = {}
        for t in transactions.get_all():
            cat_name = t.category.name
            category_sums[cat_name] = category_sums.get(cat_name, 0) + t.amount

        fig, ax = plt.subplots()
        ax.pie(category_sums.values(), labels=category_sums.keys(), autopct='%1.1f%%')
        ax.set_title("Transaction Distribution by Category", fontsize=self.font_size)
        return fig
