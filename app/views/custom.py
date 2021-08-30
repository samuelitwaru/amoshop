from PyQt5.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QPushButton, QFrame, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import QRect, Qt, QPropertyAnimation, pyqtProperty


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


class Spinner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap('app/res/icons/spinner.png')
        self.setFixedSize(100, 100)
        self._angle = 0

        self.animation = QPropertyAnimation(self, b"angle", self)
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setLoopCount(-1)
        self.animation.setDuration(1200)
        self.animation.start()

    @pyqtProperty(int)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update()

    def paintEvent(self, ev=None):
        painter = QPainter(self)
        painter.translate(50, 50)
        painter.rotate(self._angle)
        painter.translate(0, 0)
        painter.drawPixmap(0, 0, self.pixmap)
