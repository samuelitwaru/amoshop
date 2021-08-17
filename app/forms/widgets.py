from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator

class QPasswordEdit(QLineEdit):

    def __init__(self, parent=None):    
        super(QPasswordEdit, self).__init__(parent)
        self.setEchoMode(QLineEdit.Password)


class QIntegerEdit(QLineEdit):

    def __init__(self, parent=None):    
        super(QIntegerEdit, self).__init__(parent)
        self.setValidator(QIntValidator(self))
        

class QSelect(QWidget):

    def __init__(self, parent=None, choices=dict()):
        super(QSelect, self).__init__(parent)
        self.choices = choices
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout_choice_widgets()

    def layout_choice_widgets(self):
    	for k, v in self.choices.items():
    		label = v.get("label")
    		checked = v.get("checked")
    		cb = QCheckBox(label)
    		cb.setChecked(bool(checked))
    		self.layout.addWidget(cb)
    		self.choices[k]["widget"] = cb

    def clear(self):
        pass

    def get_data(self):
    	data = dict()
    	for k, v in self.choices.items():
    		checked = self.choices[k]["widget"].isChecked()
    		if checked:
    			data[k] = checked
    	return data

