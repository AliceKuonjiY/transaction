"""
交易仓库模块
"""

import json
from src.transaction import Transaction, TransactionType, Category, DateTime, CategoryType


class TransactionRepository:
    """
    交易仓库类，管理交易记录
    """
    def __init__(self, transactions: list[Transaction] = None):
        self.transactions = transactions if transactions is not None else []

    def insert(self, transaction: Transaction):
        """
        插入交易记录
        """
        self.transactions.append(transaction)

    def erase(self, transaction: Transaction):
        """
        删除交易记录
        """
        self.transactions.remove(transaction)

    def filter_by_time_range(
            self,
            start_time: DateTime,
            end_time: DateTime) -> 'TransactionRepository':
        """
        根据时间范围过滤交易记录
        @param start_time: 起始时间
        @param end_time: 结束时间
        """
        return TransactionRepository([
            t for t in self.transactions
            if start_time.__lt__(t.datetime) and t.datetime.__lt__(end_time)
        ])

    def filter_by_type(
            self,
            transaction_type: TransactionType) -> 'TransactionRepository':
        """
        根据交易类型过滤交易记录
        @param transaction_type: 交易类型
        """
        return TransactionRepository([
            t for t in self.transactions
            if t.transaction_type == transaction_type
        ])

    def filter_by_category(
            self,
            category: Category) -> 'TransactionRepository':
        """
        根据交易类别过滤交易记录
        @param category: 交易类别
        """
        return TransactionRepository([
            t for t in self.transactions
            if t.category == category
        ])

    def sort_by_datetime(self) -> 'TransactionRepository':
        """
        按时间排序交易记录
        """
        return TransactionRepository(
            sorted(self.transactions, key=lambda t: t.datetime)
        )

    def get_all(self) -> list[Transaction]:
        """
        获取所有交易记录
        """
        return self.transactions

    def get_count(self) -> int:
        """
        获取交易记录数量
        """
        return len(self.transactions)

    def clear(self):
        """
        清空交易记录
        """
        self.transactions.clear()

    def get_total_amount(self) -> float:
        """
        获取交易记录总金额
        """
        return sum(t.amount for t in self.transactions)

    def get_average_amount(self) -> float:
        """
        获取交易记录平均金额
        """
        if not self.transactions:
            return 0.0
        return self.get_total_amount() / self.get_count()

    def get_max_amount(self) -> float:
        """
        获取交易记录最大金额
        """
        if not self.transactions:
            return 0.0
        return max(t.amount for t in self.transactions)

    def get_min_amount(self) -> float:
        """
        获取交易记录最小金额
        """
        if not self.transactions:
            return 0.0
        return min(t.amount for t in self.transactions)

    def find_by_name(self, name: str) -> Transaction | None:
        """
        根据名称查找交易记录
        @param name: 交易名称
        """
        for t in self.transactions:
            if t.name == name:
                return t
        return None

    def save_to_json(self, file_path: str) -> None:
        """
        保存交易记录到JSON文件
        """
        data = []
        for t in self.transactions:
            name = t.name
            datetime = t.datetime.__str__()
            amount = t.amount
            transaction_type = t.transaction_type.value
            category = t.category.name if hasattr(t.category, "name") else t.category
            remarks = t.remarks
            data.append({
                "name": name,
                "datetime": datetime,
                "amount": amount,
                "transaction_type": transaction_type,
                "category": category,
                "remarks": remarks
            })
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_json(cls, file_path: str) -> 'TransactionRepository':
        """
        从JSON文件加载交易记录
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        transactions = []
        for d in data:
            name = d.get("name")
            datetime = DateTime.from_string(d.get("datetime"))
            amount = float(d.get("amount"))
            transaction_type = TransactionType.from_string(d.get("transaction_type"))
            category = Category(CategoryType.from_string(d.get("category")), d.get("category"))
            remarks = d.get("remarks")
            transactions.append(Transaction(name, amount, transaction_type, \
                                            category, datetime, remarks))
        return cls(transactions)
