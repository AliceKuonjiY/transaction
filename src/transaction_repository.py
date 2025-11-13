from transaction import *

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
    
    def find_by_id(self, id: str) -> Transaction | None:
        for t in self.transactions:
            if t.id == id:
                return t
        return None