from enum import Enum


class TransactionType(Enum):
    INCOME = "收入"
    EXPENSE = "支出"

    def from_string(s: str) -> 'TransactionType':
        for t in TransactionType:
            if t.value == s:
                return t
        raise ValueError(f"Unknown TransactionType: {s}")


class CategoryType(Enum):
    FOOD = "食品"
    TRANSPORT = "交通"
    ENTERTAINMENT = "娱乐"
    SALARY = "工资"
    OTHER = "其他"

    def from_string(s: str) -> 'CategoryType':
        for ct in CategoryType:
            if ct.value == s:
                return ct
        return CategoryType.OTHER


class Category:
    def __init__(
            self,
            category_type: CategoryType,
            name: str = ""):
        self.category_type = category_type
        if category_type == CategoryType.OTHER:
            self.name = name
        else:
            self.name = category_type.value


class DateTime:
    def __init__(
            self,
            year: int,
            month: int,
            day: int,
            hour: int = 0,
            minute: int = 0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def from_string(date_str: str) -> 'DateTime':
        date_part, time_part = date_str.split(" ")
        year, month, day = map(int, date_part.split("-"))
        hour, minute = map(int, time_part.split(":"))
        return DateTime(year, month, day, hour, minute)

    def __eq__(self, other):
        return (self.year == other.year and
                self.month == other.month and
                self.day == other.day)

    def __str__(self):
        return f"{self.year:04}-{self.month:02}-{self.day:02} {self.hour:02}:{self.minute:02}"
    
    def __lt__(self, other):
        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month
        if self.day != other.day:
            return self.day < other.day
        if self.hour != other.hour:
            return self.hour < other.hour
        return self.minute < other.minute


class Transaction:
    def __init__(
            self,
            name: str,
            amount: float,
            transaction_type: TransactionType,
            category: Category,
            datetime: DateTime,
            remarks: str = ""):
        self.name = name
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.datetime = datetime
        self.remarks = remarks