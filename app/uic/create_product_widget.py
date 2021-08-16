import sys
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QThread

from app.forms import CreateProductForm
from app.workers import CreateProductWorker


class CreateProductWidget(QWidget):

    def __init__(self, *args):
        super(CreateProductWidget, self).__init__(*args)
        loadUi('app/uic/uic/create_product_widget.ui', self)
        self.create_form()
        self.submitButton.clicked.connect(self.submit)


    def create_form(self):
        self.create_product_form = CreateProductForm(self.scrollLayout)
        self.form_widgets = self.create_product_form.layout_field_widgets()


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
        self.parent().parent().products_table.onDataFetched(products)
        self.progressLabel.setText("")
        self.create_product_form.clear()