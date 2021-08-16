from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QThread
from app.workers import GetSaleGroupsWorker
from app.utils import comma_separator, format_from_iso_date


class SalesWidget(QWidget):
    def __init__(self, *args):
        super(SalesWidget, self).__init__(*args)
        loadUi('app/uic/uic/sales_widget.ui', self)

        self.saleGroupsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.saleGroupsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.saleGroupsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.saleGroupsTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.saleGroupsTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.saleGroupsTable.itemSelectionChanged.connect(self.show_sales)
        self.saleGroupsTable.setColumnHidden(0, True)

        self.salesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.salesTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.salesTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.salesTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.salesTable.setSelectionBehavior(QTableWidget.SelectRows)


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
        self.saleGroupsTable.setRowCount(len(self.sale_groups))
        row = 0
        for data in self.sale_groups:
            ID = data.get("id")
            date = data.get("created_at", "")
            cashier = data.get("user").get("profile").get("name")
            amount = data.get("amount")

            self.saleGroupsTable.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.saleGroupsTable.setItem(row, 1, QTableWidgetItem(format_from_iso_date(date)))
            self.saleGroupsTable.setItem(row, 2, QTableWidgetItem(f"{cashier}"))
            self.saleGroupsTable.setItem(row, 3, QTableWidgetItem(comma_separator(amount)))
            
            row += 1

    def show_sales(self):
        currentRow = self.saleGroupsTable.currentRow()
        currentCol = 0
        ID = int(self.saleGroupsTable.item(currentRow, currentCol).text())
        sale_group = self.get_sale_group(ID)
        amount = sale_group.get("amount")
        paid = sale_group.get("paid")
        sales = sale_group.get("sales")

        self.amountLabel.setText(comma_separator(amount))
        self.paidLabel.setText(comma_separator(paid))
        self.balanceLabel.setText(comma_separator(paid-amount))
        self.load_sales(sales)

    def load_sales(self, sales):
        self.salesTable.setRowCount(len(sales))
        row = 0
        for data in sales:
            product = data.get("product").get("name")
            quantity = data.get("quantity")
            selling_price = data.get("selling_price")
            total = quantity * selling_price
            self.salesTable.setItem(row, 0, QTableWidgetItem(product))
            self.salesTable.setItem(row, 1, QTableWidgetItem(str(quantity)))
            self.salesTable.setItem(row, 2, QTableWidgetItem(comma_separator(selling_price)))
            self.salesTable.setItem(row, 3, QTableWidgetItem(comma_separator(total)))
            row += 1




