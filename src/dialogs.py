from transaction import *
from plot_service import PlotService
from PyQt5.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QDateEdit,
    QTimeEdit,
    QListWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt


matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False


class AddDialog(QDialog):
    """
    添加交易对话框
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加交易")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.type_combo = QComboBox()
        self.type_combo.addItems([t.value for t in TransactionType])
        self.category_combo = QComboBox()
        self.category_combo.addItems([t.value for t in CategoryType])
        self.amount_edit = QLineEdit()
        time_layout = QHBoxLayout()
        self.date_edit = QDateEdit()
        self.time_edit = QTimeEdit()
        time_layout.addWidget(self.date_edit)
        time_layout.addWidget(self.time_edit)
        self.remark_edit = QTextEdit()
        self.remark_edit.setFixedHeight(60)

        form.addRow(QLabel("名称："), self.name_edit)
        form.addRow(QLabel("类型："), self.type_combo)
        form.addRow(QLabel("类别："), self.category_combo)
        form.addRow(QLabel("金额："), self.amount_edit)
        form.addRow(QLabel("时间："), time_layout)
        form.addRow(QLabel("备注："), self.remark_edit)

        layout.addLayout(form)

        add_button = QPushButton("添加")
        add_button.clicked.connect(self.accept)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def get_transaction(self) -> Transaction:
        """
        获取交易对象
        """
        name = self.name_edit.text()
        transaction_type = TransactionType(self.type_combo.currentText())
        category = Category(CategoryType(self.category_combo.currentText()))
        if self.amount_edit.text() == "":
            amount = 0.0
        else:
            amount = float(self.amount_edit.text())
        date = self.date_edit.date()
        time = self.time_edit.time()
        datetime = DateTime(
            year=date.year(),
            month=date.month(),
            day=date.day(),
            hour=time.hour(),
            minute=time.minute()
        )
        remarks = self.remark_edit.toPlainText()
        return Transaction(
            name=name,
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            datetime=datetime,
            remarks=remarks
        )

    def accept(self):
        return super().accept()


class ListDialog(QDialog):
    """
    交易列表对话框
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("交易列表")
        self.setGeometry(100, 100, 600, 300)

        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        transactions = parent.transaction_repo.get_all()

        for t in transactions:
            item_text = f"名称: {t.name}  |  类型: {t.transaction_type.value}  |  金额: {t.amount}  |  时间: {t.datetime}  |  类别: {t.category.name}"
            self.list_widget.addItem(item_text)

        self.list_widget.clicked.connect(self.on_item_clicked)

        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def on_item_clicked(self, index):
        item = self.list_widget.item(index.row())
        print(f"Clicked on: {item.text()}")


class PlotDialog(QDialog):
    """
    交易图表对话框
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("交易图表")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.style_combo = QComboBox()
        self.style_combo.addItems(["bar", "line", "pie"])
        layout.addWidget(self.style_combo)
        self.style_combo.currentTextChanged.connect(self.update_plot)
        self.plot_service_bar = PlotService(style="bar")
        self.plot_service_line = PlotService(style="line")
        self.plot_service_pie = PlotService(style="pie")
        self.canvas = FigureCanvas()
        self.update_plot()
        layout.addWidget(self.canvas)
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        self.setLayout(layout)

    def update_plot(self):
        """
        更新图表
        """
        style = self.style_combo.currentText()
        transactions = self.parent().transaction_repo
        if style == "bar":
            plot_service = self.plot_service_bar
        elif style == "line":
            plot_service = self.plot_service_line
        elif style == "pie":
            plot_service = self.plot_service_pie
        else:
            return

        fig = plot_service.get_plot(transactions)
        self.canvas.figure = fig
        self.canvas.draw()