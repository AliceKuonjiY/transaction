"""
交易模块
"""

from enum import Enum


class TransactionType(Enum):
    """
    交易类型枚举
    """
    INCOME = 0
    EXPENSE = 1

    @classmethod
    def from_string(cls, s: int) -> 'TransactionType':
        """
        从字符串解析TransactionType枚举
        """
        for t in TransactionType:
            if t.value == s:
                return t
        raise ValueError(f"Unknown TransactionType: {s}")


class CategoryType(Enum):
    """
    交易类别枚举
    """
    FOOD = 0
    TRANSPORT = 1
    ENTERTAINMENT = 2
    SALARY = 3
    OTHER = 4

    @classmethod
    def from_string(cls, s: str) -> 'CategoryType':
        """
        从字符串解析CategoryType枚举
        """
        for ct in CategoryType:
            if ct.value == s:
                return ct
        return CategoryType.OTHER


class Category:
    """
    交易类别类
    """
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
    """
    自定义日期时间类
    """
    def __init__(
            self,
            year: int,
            month: int,
            day: int,
            hour: int = 0,
            minute: int = 0):
        """
        初始化DateTime对象
        @param year: 年
        @param month: 月
        @param day: 日
        @param hour: 时
        @param minute: 分
        """
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    @classmethod
    def from_string(cls, date_str: str) -> 'DateTime':
        """
        从字符串解析DateTime对象
        @param date_str: 日期时间字符串，格式为"YYYY-MM-DD HH:MM"
        """
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
    """
    交易类
    """
    def __init__(
            self,
            name: str,
            amount: float,
            transaction_type: TransactionType,
            category: Category,
            datetime: DateTime,
            remarks: str = ""):
        """
        初始化交易对象
        @param name: 交易名称
        @param amount: 交易金额
        @param transaction_type: 交易类型
        @param category: 交易类别
        @param datetime: 交易时间
        @param remarks: 备注
        """
        self.name = name
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.datetime = datetime
        self.remarks = remarks
