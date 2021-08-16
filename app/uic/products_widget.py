import sys
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QDialog, QInputDialog, QLabel, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.uic import loadUi
from app import app
from app.workers import GetProductsWorker
from app.utils import comma_separator
from app.res.rcc import product
from app.forms import CreateProductForm, UpdateProductForm
from app.workers import CreateProductWorker, UpdateProductWorker


class ProductsWidget(QWidget):
    products = []
    product = None
    def __init__(self, *args):
        super(ProductsWidget, self).__init__(*args)
        loadUi('app/uic/uic/products_widget.ui', self)
        self.productsTable.itemSelectionChanged.connect(self.show_product)
        self.productsTable.setColumnHidden(0, True)
        self.productsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.get_products_worker = GetProductsWorker()
        self.get_products_worker.onSuccess.connect(self.load_products)
        self.get_products_worker.start()
        self.newProductButton.clicked.connect(self.show_create_product_dialog)
        self.editProductButton.clicked.connect(self.show_update_product_dialog)
        self.addProductStockButton.clicked.connect(self.show_add_product_stock_dialog)
        self.create_product_widget = CreateProductWidget(parent=self)

    def load_products(self, data_list):
        self.products = data_list
        self.productsTable.setSortingEnabled(False)
        self.productsTable.setRowCount(len(data_list))
        row = 0
        for data in data_list:
            ID = data.get("id")
            name = data.get("name")
            quantity = data.get("quantity")
            units = data.get("units")
            self.productsTable.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.productsTable.setItem(row, 1, QTableWidgetItem(name))
            self.productsTable.setItem(row, 2, QTableWidgetItem(f"{comma_separator(quantity)} ({units})"))
            row += 1
        self.productsTable.setSortingEnabled(True)

    def get_product(self, item_id):
        def filter_item(item):
            return item.get("id") == item_id
        for item in list(filter(filter_item, self.products)):
            return item    

    def show_product(self):
        currentRow = self.productsTable.currentRow()
        currentCol = 0
        ID = int(self.productsTable.item(currentRow, currentCol).text())
        product = self.get_product(ID)
        self.product = product
        self.update_product_labels(product)

    def update_product_labels(self, product):
        self.productIdLabel.setText(str(product.get("id")))
        self.productNameLabel.setText(product.get("name"))
        self.productBrandLabel.setText(product.get("brand"))
        self.productBarcodeLabel.setText(product.get("barcode"))
        self.productDescriptionLabel.setText(product.get("description"))
        self.productQuantityLabel.setText(f'{product.get("quantity")} ({product.get("units")})')
        self.editProductButton.setText("Edit")
        self.addProductStockButton.setText("Add Stock")

    def show_create_product_dialog(self):
        self.create_product_widget.show()

    def show_update_product_dialog(self):
        self.update_product_widget = UpdateProductWidget(parent=self, product=self.product)
        self.update_product_widget.show()

    def show_add_product_stock_dialog(self):
        i, ok = QInputDialog.getInt(self, "Add Stock",
                f"Quantity ({self.product.get('units')})")
        if ok:
            self.integerLabel.setText("%d%%" % i)



class CreateProductWidget(QDialog):
    
    def __init__(self, parent):
        super(CreateProductWidget, self).__init__()
        self.parent = parent
        loadUi('app/uic/uic/create_product_widget.ui', self)
        self.create_product_form = CreateProductForm(self.scrollLayout)
        self.form_widgets = self.create_product_form.layout_field_widgets()
        self.submitButton.clicked.connect(self.submit)

    def submit(self):
        # get data
        data = {
            "name": self.create_product_form.widgets["name"]["input"].text(),
            "brand": self.create_product_form.widgets["brand"]["input"].text(),
            "description": self.create_product_form.widgets["description"]["input"].toPlainText(),
            "barcode": self.create_product_form.widgets["barcode"]["input"].text(),
            "buying_price": self.create_product_form.widgets["buying_price"]["input"].text(),
            "selling_price": self.create_product_form.widgets["selling_price"]["input"].text(), 
            "units": self.create_product_form.widgets["units"]["input"].text(), 
        }
        self.create_product_form.form_data = data
        if self.create_product_form.validate_form_data():
            self.create_product_worker = CreateProductWorker(data)
            self.create_product_worker.onStarted.connect(lambda: self.progressLabel.setText("Loading ..."))
            self.create_product_worker.onSuccess.connect(self.load_products)
            self.create_product_worker.onError.connect(self.onCreateProductError)
            self.create_product_worker.start()
        self.create_product_form.show_errors()

    def onCreateProductError(self, message):
        errors = message.get("message")
        self.create_product_form.errors = errors
        self.create_product_form.show_errors()
        self.progressLabel.setText("")

    def setProgressLabel(self, text):
        self.progressLabel.setText(text)

    def load_products(self, products):
        self.parent.load_products(products)
        self.progressLabel.setText("")
        self.create_product_form.clear()


class UpdateProductWidget(QDialog):
    
    def __init__(self, parent, product):
        super(UpdateProductWidget, self).__init__()
        loadUi('app/uic/uic/update_product_widget.ui', self)
        self.parent = parent
        self.product = product
        self.update_product_form = UpdateProductForm(box_layout=self.scrollLayout)
        self.update_product_form.layout_field_widgets()
        self.update_product_form.form_data = self.product
        self.update_product_form.set_widget_values()
        self.submitButton.clicked.connect(self.submit)

    def submit(self):
        # get data
        data = {
            "name": self.update_product_form.widgets["name"]["input"].text(),
            "brand": self.update_product_form.widgets["brand"]["input"].text(),
            "description": self.update_product_form.widgets["description"]["input"].toPlainText(),
            "barcode": self.update_product_form.widgets["barcode"]["input"].text(),
            "buying_price": self.update_product_form.widgets["buying_price"]["input"].text(),
            "selling_price": self.update_product_form.widgets["selling_price"]["input"].text(), 
            "units": self.update_product_form.widgets["units"]["input"].text(), 
        }
        self.update_product_form.form_data = data
        if self.update_product_form.validate_form_data():
            self.worker = UpdateProductWorker(self.product, data)
            self.worker.onStarted.connect(self.onStarted)
            self.worker.onSuccess.connect(self.onSuccess)
            self.worker.onError.connect(self.onUpdateProductError)
            self.worker.start()
        self.update_product_form.show_errors()

    def onStarted(self):
        self.progressLabel.setText("Please wait...")

    def onSuccess(self, products):
        self.parent.load_products(products)
        self.progressLabel.setText("")

    def onUpdateProductError(self, message):
        errors = message.get("message")
        self.update_product_form.errors = errors
        self.update_product_form.show_errors()
        self.progressLabel.setText("")