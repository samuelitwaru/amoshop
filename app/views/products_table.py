from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from app.utils import comma_separator
from app.workers import GetProductsWorker, DeleteProductWorker


class ProductsTable(QTableWidget):

    items = []

    def __init__(self):
        super(ProductsTable, self).__init__()
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(self.SelectRows)

        self.setColumnCount(4)
        headlables = ('ID', 'Product Name', 'Buying Price', 'Selling Price')
        self.setColumnHidden(0, True)
        self.hedprops = (0, 1, 1, 1)
        self.setHorizontalHeaderLabels(headlables)
        self.get_products_worker = GetProductsWorker()
        self.get_products_worker.onSuccess.connect(self.onDataFetched)

    def getItem(self, item_id):
        def filter_item(item):
            return item.get("id") == item_id
        for item in list(filter(filter_item, self.items)):
            return item

    def resizeEvent(self, event):
        selfsz = event.size().width()
        totalprops = sum(self.hedprops)
        newszs = [sz*selfsz/totalprops for sz in self.hedprops]
        for i, sz in enumerate(newszs):
            self.horizontalHeader().resizeSection(i, sz)

    def loadData(self, data=[]):
        self.setItem(0, 0, QTableWidgetItem("Name"))
        self.setItem(1, 0, QTableWidgetItem("Kalani"))

    def onDataFetched(self, data_list):
        self.items = data_list
        self.setSortingEnabled(False)
        self.setRowCount(len(data_list))
        row = 0
        for data in data_list:
            name = data.get("name")
            ID = data.get("id")
            selling_price = data.get("buying_price")
            buying_price = data.get("selling_price")
            self.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.setItem(row, 1, QTableWidgetItem(name))
            self.setItem(row, 2, QTableWidgetItem(comma_separator(selling_price)))
            self.setItem(row, 3, QTableWidgetItem(comma_separator(buying_price)))
            row += 1
        self.setSortingEnabled(True)

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        edit_act = contextMenu.addAction("Edit")
        edit_act.triggered.connect(self.editProduct)

        delete_act = contextMenu.addAction("Delete")
        delete_act.triggered.connect(self.deleteProduct)

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    def deleteProduct(self):
        currentRow = self.currentRow()
        currentCol = 0
        ID = int(self.item(currentRow, currentCol).text())
        item = self.getItem(ID)
        msgBox = QMessageBox(QMessageBox.Warning, "Delete Product",
                f'Are you sure you want to delete the product "{item.get("name")}"', QMessageBox.NoButton, self)
        msgBox.addButton("Yes, delete", QMessageBox.AcceptRole)
        msgBox.addButton("Cancel", QMessageBox.RejectRole)
        if msgBox.exec_() == QMessageBox.AcceptRole:
            self.delete_product_worker = DeleteProductWorker(ID)
            self.delete_product_worker.onSuccess.connect(self.onDataFetched)
            self.delete_product_worker.start()

    def editProduct(self):
        currentRow = self.currentRow()
        currentCol = 0
        ID = int(self.item(currentRow, currentCol).text())
        item = self.getItem(ID)
        self.parent().showUpdateProduct(item)
