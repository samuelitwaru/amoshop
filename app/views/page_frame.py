from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from app.uic import ProductsWidget
from app.uic import SalesWidget
from app.uic import SellingWidget
from app.uic import AccountWidget
from app.uic import UsersWidget
from app import app


class PageFrame(QStackedWidget):
    pages = dict()

    def __init__(self):
        super(PageFrame, self).__init__()
        self.initialize_ui()
        self.currentChanged.connect(self.page_changed)

    def initialize_ui(self):
        user_roles = app.user.get("roles")
        if "cashier" in user_roles:
            self.selling_widget = SellingWidget()
            num = self.addWidget(self.selling_widget)
            self.pages["selling_page"] = num
        if "admin" in user_roles:
            self.sales_widget = SalesWidget()
            num = self.addWidget(self.sales_widget)
            self.pages["sales_page"] = num
            
            self.products_widget = ProductsWidget()
            num = self.addWidget(self.products_widget)
            self.pages["products_page"] = num

            self.users_widget = UsersWidget()
            num = self.addWidget(self.users_widget)
            self.pages["users_page"] = num
        
        self.account_widget = AccountWidget()
        num = self.addWidget(self.account_widget)
        self.pages["account_page"] = num

    def page_changed(self, index):
        buttons = self.parent().main_menu.buttons
        for i in range(len(buttons)):
            if i == index:
                buttons[i].setStyleSheet("border:none;")
            else:
                buttons[i].setStyleSheet("")





