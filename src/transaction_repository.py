from transaction import *
import json
import datetime as _dt


class TransactionRepository:
    def __init__(self, transactions: list[Transaction] = None):
        self.transactions = transactions if transactions is not None else []

    def insert(self, transaction: Transaction):
        self.transactions.append(transaction)

    def erase(self, transaction: Transaction):
        self.transactions.remove(transaction)

    def filter_by_time_range(
            self,
            start_time: DateTime,
            end_time: DateTime) -> 'TransactionRepository':
        return TransactionRepository([
            t for t in self.transactions
            if start_time <= t.datetime <= end_time
        ])
    
    def filter_by_type(
            self,
            transaction_type: TransactionType) -> 'TransactionRepository':
        return TransactionRepository([
            t for t in self.transactions
            if t.transaction_type == transaction_type
        ])
    
    def filter_by_category(
            self,
            category: Category) -> 'TransactionRepository':
        return TransactionRepository([
            t for t in self.transactions
            if t.category == category
        ])
    
    def sort_by_datetime(self) -> 'TransactionRepository':
        return TransactionRepository(
            sorted(self.transactions, key=lambda t: t.datetime)
        )
    
    def get_all(self) -> list[Transaction]:
        return self.transactions
    
    def get_count(self) -> int:
        return len(self.transactions)
    
    def clear(self):
        self.transactions.clear()

    def get_total_amount(self) -> float:
        return sum(t.amount for t in self.transactions)
    
    def get_average_amount(self) -> float:
        if not self.transactions:
            return 0.0
        return self.get_total_amount() / self.get_count()
    
    def get_max_amount(self) -> float:
        if not self.transactions:
            return 0.0
        return max(t.amount for t in self.transactions)
    
    def get_min_amount(self) -> float:
        if not self.transactions:
            return 0.0
        return min(t.amount for t in self.transactions)
    
    def find_by_name(self, name: str) -> Transaction | None:
        for t in self.transactions:
            if t.name == name:
                return t
        return None
    
    def save_to_json(self, file_path: str) -> None:
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
            transactions.append(Transaction(name, amount, transaction_type, category, datetime, remarks))
        return cls(transactions)