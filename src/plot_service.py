from matplotlib import pyplot as plt
from transaction_repository import TransactionRepository
from transaction import *


class PlotService:
    def __init__(
            self,
            style: str = "bar",
            font_size: int = 12):
        self.style = style
        self.font_size = font_size

    def get_plot(self, transactions: TransactionRepository) -> plt.Figure:
        if self.style == "bar":
            return self._create_bar_plot(transactions)
        elif self.style == "line":
            return self._create_line_plot(transactions)
        elif self.style == "pie":
            return self._create_pie_chart(transactions)
        else:
            raise ValueError(f"Unknown plot style: {self.style}")
        
    def _create_bar_plot(self, transactions: TransactionRepository) -> plt.Figure:
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
        category_sums = {}
        for t in transactions.get_all():
            cat_name = t.category.name
            category_sums[cat_name] = category_sums.get(cat_name, 0) + t.amount
        
        fig, ax = plt.subplots()
        ax.pie(category_sums.values(), labels=category_sums.keys(), autopct='%1.1f%%')
        ax.set_title("Transaction Distribution by Category", fontsize=self.font_size)
        return fig