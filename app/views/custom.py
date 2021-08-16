from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from app.res.style import *

class LineEdit(QWidget):
    label = None
    line_edit = None

    def __init__(self, label_text=str(), line_edit_text=str()):
        super(LineEdit, self).__init__()
        self.label_text = label_text
        self.line_edit_text = line_edit_text
        self.initialize_ui()

    def initialize_ui(self):
        v_layout = QVBoxLayout()
        self.setLayout(v_layout)

        self.label = QLabel(self, text=self.label_text)
        self.line_edit = QLineEdit(self, text=self.line_edit_text)

        v_layout.addWidget(self.label)
        v_layout.addWidget(self.line_edit)


class ImageButton(QPushButton):
    image = None
    label = None

    def __init__(self, image_path=str('app/res/icons/products.png'), image_size=50, button_text=str()):
        super(ImageButton, self).__init__()
        self.image_path = image_path
        self.button_text = button_text
        self.image_size = image_size
        self.initialize_ui()

    def initialize_ui(self):
        v_layout = QVBoxLayout()
        self.setLayout(v_layout)

        pixmap = QIcon(self.image_path).pixmap(self.image_size, self.image_size)
        self.image = QLabel(self, pixmap=pixmap, alignment=Qt.AlignCenter)
        self.label = QLabel(self, text=self.button_text, alignment=Qt.AlignCenter)

        v_layout.addWidget(self.image)
        v_layout.addWidget(self.label)


class Horizontal(QFrame):

    def __init__(self):
        super().__init__()
        self.setGeometry(QRect(320, 150, 118, 3))
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Raised)


class Vertical(QFrame):

    def __init__(self):
        super().__init__()
        self.setGeometry(QRect(320, 150, 118, 3))
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Raised)


class Spinner(QLabel):

    def __init__(self, parent=None):
        super(Spinner, self).__init__(parent)
        # self.setPixmap(QIcon('app/res/icons/loading.gif').pixmap(50, 50))
        # self.setStyleSheet(f"{p_5}{bg_primary}")
        self.setText("- - - - - - - - - -")
        self.do_anim()

    def do_anim(self):
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(2000)
        self.anim.setStartValue(QPoint(-400, 40))
        self.anim.setEndValue(QPoint(600, 40))
        self.anim.setLoopCount(-1)

        self.anim.start()
