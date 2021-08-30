from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtCore import QSize
from app.views.custom import ImageButton

from app import app
from app.res.rcc import icons


class MainMenu(QFrame):

    def __init__(self, page_frame):
        super().__init__()
        self.buttons = []
        self.page_frame= page_frame
        self.layout = self.set_layout()
        self.initialize_ui()

    def set_layout(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        return layout

    def initialize_ui(self):
        user_roles = app.user.get("roles")

        if "cashier" in user_roles:
            self.selling_btn = ImageButton(image_path=":/icons/selling.png", image_size=50, button_text="Sell")
            self.selling_btn.setMinimumSize(QSize(100, 100))
            self.selling_btn.clicked.connect(lambda: self.page_frame.setCurrentIndex(self.page_frame.pages["selling_page"]))
            self.layout.addWidget(self.selling_btn)
            self.buttons.append(self.selling_btn)
        
        if "admin" in user_roles:
            self.sales_btn = ImageButton(image_path=":/icons/sales.png", image_size=50, button_text="Sales")
            self.sales_btn.setMinimumSize(QSize(100, 100))
            self.sales_btn.clicked.connect(lambda: self.page_frame.setCurrentIndex(self.page_frame.pages["sales_page"]))
            self.layout.addWidget(self.sales_btn)
            self.buttons.append(self.sales_btn)

            self.products_btn = ImageButton(image_path=":/icons/products.png", image_size=50, button_text="Products")
            self.products_btn.setMinimumSize(QSize(100, 100))
            self.products_btn.clicked.connect(lambda: self.page_frame.setCurrentIndex(self.page_frame.pages["products_page"]))
            self.layout.addWidget(self.products_btn)
            self.buttons.append(self.products_btn)

            self.users_btn = ImageButton(image_path=":/icons/users.png", image_size=50, button_text="Users")
            self.users_btn.setMinimumSize(QSize(100, 100))
            self.users_btn.clicked.connect(lambda: self.page_frame.setCurrentIndex(self.page_frame.pages["users_page"]))
            self.layout.addWidget(self.users_btn)
            self.buttons.append(self.users_btn)

        self.account_btn = ImageButton(image_path=":/icons/account.png", image_size=50, button_text="Account")
        self.account_btn.setMinimumSize(QSize(100, 100))
        self.account_btn.clicked.connect(lambda: self.page_frame.setCurrentIndex(self.page_frame.pages["account_page"]))
        self.layout.addWidget(self.account_btn)
        self.buttons.append(self.account_btn)

        self.logout_btn = ImageButton(image_path=":/icons/logout.png", image_size=50, button_text="Logout")
        self.logout_btn.setMinimumSize(QSize(100, 100))
        self.logout_btn.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_btn)
        self.buttons.append(self.logout_btn)


        self.layout.addStretch()


    def logout(self):
        self.parent().destroy()
        self.parent().setParent(None)


