
import frelatage
import random
from transaction import Transaction, TransactionType, Category, CategoryType, DateTime


# 自定义随机数据生成函数
def create_random_transaction_input():
    """
    使用 frelatage.Input 创建随机交易的输入数据
    """
    transaction_data = {
        "name": f"Transaction {random.randint(1, 1000)}",
        "amount": random.uniform(-1000, 1000),
        "transaction_type": random.choice(list(TransactionType)).value,  # 使用字符串值
        "category_type": random.choice(list(CategoryType)).value,       # 使用字符串值
        "year": random.randint(2000, 2030),
        "month": random.randint(1, 12),
        "day": random.randint(1, 28),
        "hour": random.randint(0, 23),
        "minute": random.randint(0, 59),
        "remarks": f"Remarks {random.randint(1, 1000)}",
    }
    return frelatage.Input(str(transaction_data))  # 转为字符串并用 Input 包装

# 模糊测试函数
def test_transaction_repository(i1, i2, i3, i4, i5, i6,i7, i8, i9, i10):
    """
    对 TransactionRepository 类进行模糊测试
    """
    from transaction_repository import TransactionRepository

    # 创建 TransactionRepository 对象并插入交易
    repository = TransactionRepository()
    repository.insert(Transaction(i1, i2, i3, i4, DateTime(i5, i6, i7, i8, i9), i10))  # 将输入数据转换为 Transaction 对象

# 构造初始 corpus（种子数据）
corpus = [
    [frelatage.Input("str")],
    [frelatage.Input(100)],
    [frelatage.Input(0)],
    [frelatage.Input(1)],
    [frelatage.Input(1)],
    [frelatage.Input(1)],
    [frelatage.Input(1)],
    [frelatage.Input(1)],
    [frelatage.Input(1)],
    [frelatage.Input("str")],
]

# 使用 frelatage 进行模糊测试
fuzz = frelatage.Fuzzer(
    method=test_transaction_repository,
    corpus=corpus,
    threads_count=4,
    output_directory="./fuzz_output",
    silent=False,
    infinite_fuzz=True,
)
fuzz.fuzz()
