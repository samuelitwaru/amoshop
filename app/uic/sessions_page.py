import sys
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.uic import loadUi


class SessionsPage(QWidget):
    def __init__(self, *args):
        super(SessionsPage, self).__init__(*args)
        loadUi('app/uic/uic/sessions_page.ui', self)