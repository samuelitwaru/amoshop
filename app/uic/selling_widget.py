from PyQt5.QtWidgets import QWidget, QLabel, QTableWidgetItem, QTableWidget, QMessageBox, QHeaderView, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import *
from app.utils import comma_separator
from app import app
# from app.workers import SearchProductWorker, CheckoutWorker, GetProductsWorker
from app.models import session, Product, product_schema, load_products
from app.uic.uic.selling_widget import Ui_Form
from app.workers import SendRequestWorker
from app.api import urls
import requests


class SellingWidget(QWidget):
    
    def __init__(self, *args):
        super(SellingWidget, self).__init__(*args)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # init state data
        self.sales = {
            "amount": 0,
            "paid": 0,
            "cart": dict()
        }
        self.session = None
        self.products = None

        self.get_products_worker = SendRequestWorker(urls.product_list, requests.get)
        self.get_products_worker.onSuccessList.connect(load_products)
        self.get_products_worker.start()

        # setup ui
        self.ui.searchLineEdit.textChanged.connect(self.search_product_2)
        self.ui.clearButton.clicked.connect(self.clear_cart)
        self.ui.checkoutButton.clicked.connect(self.checkout)
        # setup productsTable
        self.ui.productsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.productsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.productsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.ui.productsTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.ui.productsTable.setColumnHidden(0, True)
        # setup cartTable
        self.ui.cartTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.cartTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.cartTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.ui.cartTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.ui.cartTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.ui.cartTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.ui.cartTable.setColumnHidden(0, True)
        # setup amountLineEdit
        self.ui.amountLineEdit.setValidator(QIntValidator(self.ui.amountLineEdit))
        self.ui.amountLineEdit.textChanged.connect(self.setBalance)
        self.ui.amountLineEdit.returnPressed.connect(self.checkout)
        
    def search_product(self):
        query_string = self.ui.searchLineEdit.text()
        if query_string:
            self.worker = SearchProductWorker(query_string)
            self.worker.onSuccess.connect(self.onSearchResult)
            self.worker.start()

    def search_product_2(self):
        query_string = self.ui.searchLineEdit.text()
        products = []
        if query_string:
            query = session.query(Product).filter(Product.barcode==query_string)
            if not query.first():
                query = session.query(Product).filter(Product.name.like(f'%{query_string}%'))
            self.onSearchResult(query.all())
        else:
            self.onSearchResult(session.query(Product).all())

    def onSearchResult(self, data_list):
        if len(data_list) == 1:
            self.add_to_cart_2(data_list[0])
            self.ui.searchLineEdit.clear()
        self.products = data_list
        self.load_products_2()

    def add_to_cart(self, product):
        cart_product = self.sales.get('cart').get(product.get("id"))
        if cart_product:
            cart_product["quantity"] += 1
        else:
            self.sales.get('cart')[product.get("id")] = product
            self.sales.get('cart')[product.get("id")]["quantity"] = 1
        self.refresh_cart()

    def add_to_cart_2(self, product):
        cart_product = self.sales.get('cart').get(product.id)
        if cart_product:
            cart_product["quantity"] += 1
        else:
            self.sales.get('cart')[product.id] = product_schema.dump(product)
            self.sales.get('cart')[product.id]["quantity"] = 1
        self.refresh_cart()

    def remove_from_cart(self, product_id):
        cart_product = self.sales.get('cart').get(product_id)
        quantity = cart_product["quantity"]
        if quantity == 1:
            self.sales.get('cart').pop(product_id)
        else:
            cart_product["quantity"] -= 1
        self.refresh_cart()

    def remove_from_cart_2(self, product_id):
        cart_product = self.sales.get('cart').get(product_id)
        quantity = cart_product.quantity
        if quantity == 1:
            self.sales.get('cart').pop(product_id)
        else:
            cart_product.quantity -= 1
        self.refresh_cart_2()

    def clear_cart(self, sales):
        self.sales = {
            "amount": 0,
            "paid": 0,
            "cart": dict()
        }
        self.ui.amountLineEdit.clear()
        self.refresh_cart()
        self.ui.searchLineEdit.setFocus()

    def refresh_cart(self):
        self.ui.cartTable.setRowCount(len(self.sales.get('cart')))
        row = 0
        amount = 0
        for ID, data in self.sales.get('cart').items():
            name = data.get("name")
            quantity = data.get("quantity")
            unit_price = data.get("selling_price")
            total = unit_price * quantity
            amount += total
            removeFromCartButton = QPushButton(text="-")
            removeFromCartButton.setStyleSheet("margin:2px;") 
            removeFromCartButton.clicked.connect(
                lambda: self.remove_from_cart (
                        int(self.ui.cartTable.item(self.ui.cartTable.currentRow(), 0).text())
                    )
                )
            self.ui.cartTable.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.ui.cartTable.setCellWidget(row, 1, removeFromCartButton)
            self.ui.cartTable.setItem(row, 2, QTableWidgetItem(name))
            self.ui.cartTable.setItem(row, 3, QTableWidgetItem(comma_separator(quantity)))
            self.ui.cartTable.setItem(row, 4, QTableWidgetItem(comma_separator(unit_price)))
            self.ui.cartTable.setItem(row, 5, QTableWidgetItem(comma_separator(total)))
            row += 1
        self.sales['amount'] = amount
        self.ui.amountLabel.setText(comma_separator(amount))
        self.setBalance()

    def refresh_cart_2(self):
        self.ui.cartTable.setRowCount(len(self.sales.get('cart')))
        row = 0
        amount = 0
        for ID, product in self.sales.get('cart').items():
            total = product.selling_price * product.quantity
            amount += total
            removeFromCartButton = QPushButton(text="-")
            removeFromCartButton.setStyleSheet("margin:2px;") 
            removeFromCartButton.clicked.connect(
                lambda: self.remove_from_cart_2 (
                        int(self.ui.cartTable.item(self.ui.cartTable.currentRow(), 0).text())
                    )
                )
            self.ui.cartTable.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.ui.cartTable.setCellWidget(row, 1, removeFromCartButton)
            self.ui.cartTable.setItem(row, 2, QTableWidgetItem(product.name))
            self.ui.cartTable.setItem(row, 3, QTableWidgetItem(comma_separator(product.quantity)))
            self.ui.cartTable.setItem(row, 4, QTableWidgetItem(comma_separator(product.selling_price)))
            self.ui.cartTable.setItem(row, 5, QTableWidgetItem(comma_separator(total)))
            row += 1
        self.sales['amount'] = amount
        self.ui.amountLabel.setText(comma_separator(amount))
        self.setBalance()

    def load_products(self):
        self.ui.productsTable.setRowCount(len(self.products))
        row = 0
        for data in self.products:
            ID = data.get("id")
            name = data.get("name")
            brand = data.get("brand")
            addToCartButton = QPushButton(text="+")
            addToCartButton.setStyleSheet("margin:2px; background:blue;")
            addToCartButton.clicked.connect(
                lambda: self.add_to_cart (
                        self.get_product_by_id (
                            int(self.ui.productsTable.item(self.ui.productsTable.currentRow(), 0).text())
                        )
                    )
                )
            self.ui.productsTable.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.ui.productsTable.setItem(row, 1, QTableWidgetItem(name))
            self.ui.productsTable.setItem(row, 2, QTableWidgetItem(brand))
            self.ui.productsTable.setCellWidget(row, 3, addToCartButton)

            row += 1

    def load_products_2(self):
        self.ui.productsTable.setRowCount(len(self.products))
        row = 0
        for product in self.products:
            addToCartButton = QPushButton(text="+")
            addToCartButton.setStyleSheet("margin:2px; background:blue;")
            addToCartButton.clicked.connect(
                lambda: self.add_to_cart_2 (
                        self.get_product_by_id_2 (
                            int(self.ui.productsTable.item(self.ui.productsTable.currentRow(), 0).text())
                        )
                    )
                )
            self.ui.productsTable.setItem(row, 0, QTableWidgetItem(str(product.id)))
            self.ui.productsTable.setItem(row, 1, QTableWidgetItem(product.name))
            self.ui.productsTable.setItem(row, 2, QTableWidgetItem(comma_separator(product.selling_price)))
            self.ui.productsTable.setCellWidget(row, 3, addToCartButton)
            row += 1
            
    def checkout(self):
        if self.sales["paid"] < self.sales["amount"]:
            reply = QMessageBox.information(self,
                    "Invalid amount", f"Invalid amount paid. It should be atleast {comma_separator(self.sales['amount'])}") 
        else:
            message = "Check out the following products?\n\n"
            for ID, product in self.sales.get('cart').items():
                message += f"{product.get('name')} ({product.get('quantity')}):         {product.get('selling_price')*product.get('quantity')}\n"
        
            reply = QMessageBox.question(self, "Confirm Checkout",
                    message,
                    QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.sales["session"] = self.session
                self.checkout_worker = SendRequestWorker(urls.sale_checkout, requests.post, json=self.sales)
                self.checkout_worker.onSuccessList.connect(self.clear_cart)
                self.checkout_worker.start()
            elif reply == QMessageBox.No:
                pass
            else:
                pass

    def checkout_2(self):
        message = "Check out the following products?\n\n"
        for ID, product in self.sales.get('cart').items():
            message += f"{product.name} ({product.quantity}):   {product.selling_price*product.quantity}\n"
        
        reply = QMessageBox.question(self, "Confirm Checkout",
                message,
                QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sales["session"] = self.session
            self.checkout_worker = SendRequestWorker(urls.sale_checkout, requests.post, json=self.sales)
            self.checkout_worker.onSuccessList.connect(self.clear_cart)
            self.checkout_worker.start()
        elif reply == QMessageBox.No:
            pass
        else:
            pass
        
    def setBalance(self):
        paid = self.ui.amountLineEdit.text() or 0
        self.sales["paid"] = int(paid)
        balance = int(paid)-self.sales.get('amount')
        self.ui.balanceLabel.setText(comma_separator(balance))

        if balance < 0:
            self.ui.balanceLabel.setStyleSheet("color:red;")
        else:
            self.ui.balanceLabel.setStyleSheet("color:green;")

    def get_product_by_id(self, product_id):
        def filter_product(product):
            return product.get("id") == product_id
        return list(filter(filter_product, self.products))[0]

    def get_product_by_id_2(self, product_id):
        def filter_product(product):
            return product.id == product_id
        return list(filter(filter_product, self.products))[0]
