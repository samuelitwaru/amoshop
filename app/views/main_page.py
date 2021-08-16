from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from app.uic import TopBar
from app.views.main_menu import MainMenu
from app.views.page_frame import PageFrame

from app.views.custom import Horizontal, Vertical


class MainPage(QWidget):

    def __init__(self, user):
        super(MainPage, self).__init__()
        self.user = user
        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()
        self.set_layout()
        self.set_ui()

    def set_layout(self):
        self.setLayout(self.v_layout)

    def set_ui(self):
        top_bar = TopBar()
        horizontal1 = Horizontal()
        # horizontal2 = Horizontal()
        vertical = Vertical()
        self.page_frame = PageFrame()

        self.main_menu = MainMenu(self.page_frame)
        self.v_layout.addWidget(top_bar, 1)
        self.v_layout.addWidget(horizontal1, 1)
        self.v_layout.addLayout(self.h_layout, 11)
        # self.v_layout.addWidget(horizontal2, 1)
        
        self.h_layout.addWidget(self.main_menu, 1)
        self.h_layout.addWidget(vertical)
        self.h_layout.addWidget(self.page_frame, 7)

