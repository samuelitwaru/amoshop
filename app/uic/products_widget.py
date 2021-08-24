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
from app.workers import CreateProductWorker, UpdateProductWorker, UpdateProductQuantityWorker
from app.uic.uic.products_widget import Ui_Form as products_widget_Ui_Form
from app.uic.uic.create_product_widget import Ui_Form as create_product_widget_Ui_Form
from app.uic.uic.update_product_widget import Ui_Form as update_product_widget_Ui_Form



class ProductsWidget(QWidget):
    products = []
    product = None
    def __init__(self, *args):
        super(ProductsWidget, self).__init__(*args)
        self.ui = products_widget_Ui_Form()
        self.ui.setupUi(self)

        self.ui.productsTable.itemSelectionChanged.connect(self.show_product)
        self.ui.productsTable.setColumnHidden(0, True)
        self.ui.productsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.productsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.get_products_worker = GetProductsWorker()
        self.get_products_worker.onSuccess.connect(self.load_products)
        self.get_products_worker.start()
        self.ui.newProductButton.clicked.connect(self.show_create_product_dialog)
        self.ui.editProductButton.clicked.connect(self.show_update_product_dialog)
        self.ui.addProductStockButton.clicked.connect(self.show_add_product_stock_dialog)
        self.create_product_widget = CreateProductWidget(parent=self)

    def load_products(self, data_list):
        self.products = data_list
        self.ui.productsTable.setSortingEnabled(False)
        self.ui.productsTable.setRowCount(len(data_list))
        row = 0
        for data in data_list:
            ID = data.get("id")
            name = data.get("name")
            quantity = data.get("quantity")
            units = data.get("units")
            self.ui.productsTable.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.ui.productsTable.setItem(row, 1, QTableWidgetItem(name))
            self.ui.productsTable.setItem(row, 2, QTableWidgetItem(f"{comma_separator(quantity)} ({units})"))
            row += 1
        self.ui.productsTable.setSortingEnabled(True)

    def get_product(self, item_id):
        def filter_item(item):
            return item.get("id") == item_id
        for item in list(filter(filter_item, self.products)):
            return item    

    def show_product(self):
        currentRow = self.ui.productsTable.currentRow()
        currentCol = 0
        ID = int(self.ui.productsTable.item(currentRow, currentCol).text())
        product = self.get_product(ID)
        self.product = product
        self.update_product_labels(product)

    def update_product_labels(self, product):
        self.ui.productIdLabel.setText(str(product.get("id")))
        self.ui.productNameLabel.setText(product.get("name"))
        self.ui.productBrandLabel.setText(product.get("brand"))
        self.ui.productBarcodeLabel.setText(product.get("barcode"))
        self.ui.buyingPriceLabel.setText(f"{comma_separator(product.get('buying_price'))} (Buying)")
        self.ui.sellingPriceLabel.setText(f'{comma_separator(product.get("selling_price"))} (Selling)')
        self.ui.productDescriptionLabel.setText(product.get("description"))
        self.ui.productQuantityLabel.setText(f'{product.get("quantity")} ({product.get("units")})')
        self.ui.editProductButton.setText("Edit")
        self.ui.addProductStockButton.setText("Add Stock")

    def show_create_product_dialog(self):
        self.create_product_widget.show()

    def show_update_product_dialog(self):
        self.update_product_widget = UpdateProductWidget(parent=self, product=self.product)
        self.update_product_widget.show()

    def show_add_product_stock_dialog(self):
        i, ok = QInputDialog.getInt(self, "Add Stock",
                f"Quantity ({self.product.get('units')})")
        if ok:
            data = {"quantity": i}
            self.worker = UpdateProductQuantityWorker(self.product, data)
            self.worker.onSuccess.connect(self.onUpdateProductQuantitySuccess)
            self.worker.start()

    def onUpdateProductQuantitySuccess(self, products):
        self.load_products(products)
        self.show_product()



class CreateProductWidget(QDialog):
    
    def __init__(self, parent):
        super(CreateProductWidget, self).__init__()
        self.parent = parent
        self.ui = create_product_widget_Ui_Form()
        self.ui.setupUi(self)
        self.create_product_form = CreateProductForm(self.ui.scrollLayout)
        self.form_widgets = self.create_product_form.layout_field_widgets()
        self.ui.submitButton.clicked.connect(self.submit)

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
            self.create_product_worker.onStarted.connect(lambda: self.ui.progressLabel.setText("Loading ..."))
            self.create_product_worker.onSuccess.connect(self.load_products)
            self.create_product_worker.onError.connect(self.onCreateProductError)
            self.create_product_worker.start()
        self.create_product_form.show_errors()

    def onCreateProductError(self, message):
        errors = message.get("message")
        self.create_product_form.errors = errors
        self.create_product_form.show_errors()
        self.ui.progressLabel.setText("")

    def setProgressLabel(self, text):
        self.ui.progressLabel.setText(text)

    def load_products(self, products):
        self.parent.load_products(products)
        self.ui.progressLabel.setText("")
        self.create_product_form.clear()


class UpdateProductWidget(QDialog):
    
    def __init__(self, parent, product):
        super(UpdateProductWidget, self).__init__()
        self.ui = update_product_widget_Ui_Form()
        self.ui.setupUi(self)
        self.parent = parent
        self.product = product
        self.update_product_form = UpdateProductForm(box_layout=self.ui.scrollLayout)
        self.update_product_form.layout_field_widgets()
        self.update_product_form.form_data = self.product
        self.update_product_form.set_widget_values()
        self.ui.submitButton.clicked.connect(self.submit)

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
        self.ui.progressLabel.setText("Please wait...")

    def onSuccess(self, products):
        self.parent.load_products(products)
        self.ui.progressLabel.setText("")

    def onUpdateProductError(self, message):
        errors = message.get("message")
        self.update_product_form.errors = errors
        self.update_product_form.show_errors()
        self.ui.progressLabel.setText("")