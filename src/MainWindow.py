from transaction_repository import TransactionRepository
from transaction import *
from dialogs import AddDialog, ListDialog, PlotDialog
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QDialog
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)
        self.transaction_repo = TransactionRepository()
        
        self.update_summary()

    def update_summary(self):
        sample_info = QVBoxLayout()
        sample_info.addWidget(QLabel("总收入：" + str(self.transaction_repo.filter_by_type(TransactionType.INCOME).get_total_amount())))
        sample_info.addWidget(QLabel("总支出：" + str(self.transaction_repo.filter_by_type(TransactionType.EXPENSE).get_total_amount())))
        sample_info.addWidget(QLabel("交易总数：" + str(self.transaction_repo.get_count())))
        sample_info.addWidget(QLabel("余额：" +
                                     str(self.transaction_repo.filter_by_type(TransactionType.INCOME).get_total_amount() -
                                         self.transaction_repo.filter_by_type(TransactionType.EXPENSE).get_total_amount())))

        button_layout = QHBoxLayout()
        add_button = QPushButton("添加交易")
        add_button.setFixedHeight(40)
        add_button.setFixedWidth(100)
        add_button.clicked.connect(self.add_transaction)
        list_button = QPushButton("交易列表")
        list_button.setFixedHeight(40)
        list_button.setFixedWidth(100)
        list_button.clicked.connect(self.show_list)
        plot_button = QPushButton("显示图表")
        plot_button.setFixedHeight(40)
        plot_button.setFixedWidth(100)
        plot_button.clicked.connect(self.show_plot)
        save_button = QPushButton("保存数据")
        save_button.setFixedHeight(40)
        save_button.setFixedWidth(100)
        save_button.clicked.connect(self.save_data)
        load_button = QPushButton("加载数据")
        load_button.setFixedHeight(40)
        load_button.setFixedWidth(100)
        load_button.clicked.connect(self.load_data)
        button_layout.addWidget(add_button)
        button_layout.addWidget(list_button)
        button_layout.addWidget(plot_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(load_button)

        self.setCentralWidget(QWidget())
        main_layout = QVBoxLayout()
        main_layout.addLayout(sample_info)
        main_layout.addLayout(button_layout)
        self.centralWidget().setLayout(main_layout)

    def add_transaction(self):
        print("添加交易按钮被点击")
        dialog = AddDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            transaction = dialog.get_transaction()
            if transaction.amount == 0.0:
                print("金额不能为空或零")
                return
            self.transaction_repo.insert(transaction)
            self.update_summary()
            print("交易已添加")

    def show_list(self):
        print("交易列表按钮被点击")
        dialog = ListDialog(self)
        dialog.exec_()

    def show_plot(self):
        print("显示图表按钮被点击")
        dialog = PlotDialog(self)
        dialog.exec_()


    def save_data(self):
        print("保存数据按钮被点击")
        self.transaction_repo.save_to_json("transactions.json")

    def load_data(self):
        print("加载数据按钮被点击")
        self.transaction_repo = TransactionRepository.load_from_json("transactions.json")
        self.update_summary()