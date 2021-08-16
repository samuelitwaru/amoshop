from PyQt5.QtWidgets import QWidget, QLabel, QTableWidgetItem, QTableWidget, QMessageBox, QHeaderView, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import *
from app.utils import comma_separator
from app import app
from app.workers import CreateUserSessionWorker, GetUserSessionWorker, EndSessionWorker, SearchProductWorker, CheckoutWorker
from app.models import session, Product, product_schema

class SellingWidget(QWidget):
    
    def __init__(self, *args):
        super(SellingWidget, self).__init__(*args)
        loadUi('app/uic/uic/selling_widget2.ui', self)
        
        # init state data
        self.sales = {
            "amount": 0,
            "paid": 0,
            "cart": dict()
        }
        self.session = None
        self.products = None

        # setup ui
        self.searchLineEdit.textChanged.connect(self.search_product_2)
        self.clearButton.clicked.connect(self.clear_cart)
        self.checkoutButton.clicked.connect(self.checkout)
        # setup productsTable
        self.productsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.productsTable.setColumnHidden(0, True)
        # setup cartTable
        self.cartTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.cartTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cartTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.cartTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.cartTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.cartTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.cartTable.setColumnHidden(0, True)
        # setup amountLineEdit
        self.amountLineEdit.setValidator(QIntValidator(self.amountLineEdit))
        self.amountLineEdit.textChanged.connect(self.setBalance)
        self.amountLineEdit.returnPressed.connect(self.checkout)
        # setup session
        # self.startSessionButton.clicked.connect(self.start_user_session)
        # self.endSessionButton.clicked.connect(self.end_session)

    def search_product(self):
        query_string = self.searchLineEdit.text()
        if query_string:
            self.worker = SearchProductWorker(query_string)
            self.worker.onSuccess.connect(self.onSearchResult)
            self.worker.start()

    def search_product_2(self):
        query_string = self.searchLineEdit.text()
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
            self.searchLineEdit.clear()
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
        self.amountLineEdit.clear()
        self.refresh_cart()
        self.searchLineEdit.setFocus()

    def refresh_cart(self):
        self.cartTable.setRowCount(len(self.sales.get('cart')))
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
                        int(self.cartTable.item(self.cartTable.currentRow(), 0).text())
                    )
                )
            self.cartTable.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.cartTable.setCellWidget(row, 1, removeFromCartButton)
            self.cartTable.setItem(row, 2, QTableWidgetItem(name))
            self.cartTable.setItem(row, 3, QTableWidgetItem(comma_separator(quantity)))
            self.cartTable.setItem(row, 4, QTableWidgetItem(comma_separator(unit_price)))
            self.cartTable.setItem(row, 5, QTableWidgetItem(comma_separator(total)))
            row += 1
        self.sales['amount'] = amount
        self.amountLabel.setText(comma_separator(amount))
        self.setBalance()

    def refresh_cart_2(self):
        self.cartTable.setRowCount(len(self.sales.get('cart')))
        row = 0
        amount = 0
        for ID, product in self.sales.get('cart').items():
            total = product.selling_price * product.quantity
            amount += total
            removeFromCartButton = QPushButton(text="-")
            removeFromCartButton.setStyleSheet("margin:2px;") 
            removeFromCartButton.clicked.connect(
                lambda: self.remove_from_cart_2 (
                        int(self.cartTable.item(self.cartTable.currentRow(), 0).text())
                    )
                )
            self.cartTable.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.cartTable.setCellWidget(row, 1, removeFromCartButton)
            self.cartTable.setItem(row, 2, QTableWidgetItem(product.name))
            self.cartTable.setItem(row, 3, QTableWidgetItem(comma_separator(product.quantity)))
            self.cartTable.setItem(row, 4, QTableWidgetItem(comma_separator(product.selling_price)))
            self.cartTable.setItem(row, 5, QTableWidgetItem(comma_separator(total)))
            row += 1
        self.sales['amount'] = amount
        self.amountLabel.setText(comma_separator(amount))
        self.setBalance()

    def load_products(self):
        self.productsTable.setRowCount(len(self.products))
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
                            int(self.productsTable.item(self.productsTable.currentRow(), 0).text())
                        )
                    )
                )
            self.productsTable.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.productsTable.setItem(row, 1, QTableWidgetItem(name))
            self.productsTable.setItem(row, 2, QTableWidgetItem(brand))
            self.productsTable.setCellWidget(row, 3, addToCartButton)

            row += 1

    def load_products_2(self):
        self.productsTable.setRowCount(len(self.products))
        row = 0
        for product in self.products:
            addToCartButton = QPushButton(text="+")
            addToCartButton.setStyleSheet("margin:2px; background:blue;")
            addToCartButton.clicked.connect(
                lambda: self.add_to_cart_2 (
                        self.get_product_by_id_2 (
                            int(self.productsTable.item(self.productsTable.currentRow(), 0).text())
                        )
                    )
                )
            self.productsTable.setItem(row, 0, QTableWidgetItem(str(product.id)))
            self.productsTable.setItem(row, 1, QTableWidgetItem(product.name))
            self.productsTable.setItem(row, 2, QTableWidgetItem(product.brand))
            self.productsTable.setCellWidget(row, 3, addToCartButton)
            row += 1
            
    def checkout(self):
        message = "Check out the following products?\n\n"
        for ID, product in self.sales.get('cart').items():
            message += f"{product.get('name')} ({product.get('quantity')}):         {product.get('selling_price')*product.get('quantity')}\n"
        
        reply = QMessageBox.question(self, "Confirm Checkout",
                message,
                QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sales["session"] = self.session
            self.checkout_worker = CheckoutWorker(self.sales)
            self.checkout_worker.onSuccess.connect(self.clear_cart)
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
            self.checkout_worker = CheckoutWorker(self.sales)
            self.checkout_worker.onSuccess.connect(self.clear_cart)
            self.checkout_worker.start()
        elif reply == QMessageBox.No:
            pass
        else:
            pass
        
    def setBalance(self):
        paid = self.amountLineEdit.text() or 0
        self.sales["paid"] = paid
        balance = int(paid)-self.sales.get('amount')
        self.balanceLabel.setText(comma_separator(balance))

        if balance < 0:
            self.balanceLabel.setStyleSheet("color:red;")
        else:
            self.balanceLabel.setStyleSheet("color:green;")

    def get_product_by_id(self, product_id):
        def filter_product(product):
            return product.get("id") == product_id
        return list(filter(filter_product, self.products))[0]

    def get_product_by_id_2(self, product_id):
        def filter_product(product):
            return product.id == product_id
        return list(filter(filter_product, self.products))[0]
