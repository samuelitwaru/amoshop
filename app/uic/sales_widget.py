from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QThread
from app.workers import GetSaleGroupsWorker
from app.utils import comma_separator, format_from_iso_date
from app.uic.uic.sales_widget import Ui_Form


class SalesWidget(QWidget):
    def __init__(self, *args):
        super(SalesWidget, self).__init__(*args)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.saleGroupsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.saleGroupsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.saleGroupsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.ui.saleGroupsTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.ui.saleGroupsTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.ui.saleGroupsTable.itemSelectionChanged.connect(self.show_sales)
        self.ui.saleGroupsTable.setColumnHidden(0, True)

        self.ui.salesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.salesTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.salesTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.ui.salesTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.ui.salesTable.setSelectionBehavior(QTableWidget.SelectRows)


        self.get_sale_groups_worker = GetSaleGroupsWorker()
        self.get_sale_groups_worker.onSuccess.connect(self.load_sale_groups)
        self.get_sale_groups_worker.start()

    def get_sale_group(self, sale_group_id):
        def filter_item(item):
            return item.get("id") == sale_group_id
        for item in list(filter(filter_item, self.sale_groups)):
            return item

    def load_sale_groups(self, sale_groups):
        self.sale_groups = sale_groups
        self.ui.saleGroupsTable.setRowCount(len(self.sale_groups))
        row = 0
        for data in self.sale_groups:
            ID = data.get("id")
            date = data.get("created_at", "")
            cashier = data.get("user").get("profile").get("name")
            amount = data.get("amount")

            self.ui.saleGroupsTable.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.ui.saleGroupsTable.setItem(row, 1, QTableWidgetItem(format_from_iso_date(date)))
            self.ui.saleGroupsTable.setItem(row, 2, QTableWidgetItem(f"{cashier}"))
            self.ui.saleGroupsTable.setItem(row, 3, QTableWidgetItem(comma_separator(amount)))
            
            row += 1

    def show_sales(self):
        currentRow = self.ui.saleGroupsTable.currentRow()
        currentCol = 0
        ID = int(self.ui.saleGroupsTable.item(currentRow, currentCol).text())
        sale_group = self.get_sale_group(ID)
        amount = sale_group.get("amount")
        paid = sale_group.get("paid")
        sales = sale_group.get("sales")

        self.ui.amountLabel.setText(comma_separator(amount))
        self.ui.paidLabel.setText(comma_separator(paid))
        self.ui.balanceLabel.setText(comma_separator(paid-amount))
        self.load_sales(sales)

    def load_sales(self, sales):
        self.ui.salesTable.setRowCount(len(sales))
        row = 0
        for data in sales:
            product = data.get("product").get("name")
            quantity = data.get("quantity")
            selling_price = data.get("selling_price")
            total = quantity * selling_price
            self.ui.salesTable.setItem(row, 0, QTableWidgetItem(product))
            self.ui.salesTable.setItem(row, 1, QTableWidgetItem(str(quantity)))
            self.ui.salesTable.setItem(row, 2, QTableWidgetItem(comma_separator(selling_price)))
            self.ui.salesTable.setItem(row, 3, QTableWidgetItem(comma_separator(total)))
            row += 1




