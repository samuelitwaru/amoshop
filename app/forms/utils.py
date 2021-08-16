from PyQt5.QtWidgets import QLineEdit, QTextEdit
from .widgets import QPasswordEdit, QSelect
from .validators import IsRequired
from PyQt5 import QtWidgets as w 
from .data import STYLES
from PyQt5.QtCore import Qt


def validator_in_validators(validator, validators):
	def filter_validator(test_validator):
		return isinstance(test_validator, validator)
	filtered = filter(filter_validator, validators)
	for validator in filtered:
		return validator


def set_widget_value(widget, value):
	if isinstance(widget, (QLineEdit, QTextEdit, QPasswordEdit)):
		widget.setText(str(value))


def get_widget_value(widget_data):
	if isinstance(widget, (QLineEdit, QPasswordEdit)):
		return widget.text()
	elif isinstance(widget, (QTextEdit)):
		return widget.toPlainText()


def render_widget(widget_data):
	asteric = ''
	if validator_in_validators(IsRequired, widget_data["validators"]):
		asteric += ' <span style="color:red">*</span>'
	label = widget_data.get("label") + asteric
	widget = widget_data.get("widget")
	default = widget_data.get("default")
	
	label_widget = w.QLabel(text=label)
	error_widget = w.QLabel(styleSheet=STYLES.get("error"), alignment=Qt.AlignRight)
	
	if widget == QSelect:
		choices = widget_data.get("choices")
		input_widget = widget(choices=choices)
	else:
		input_widget = widget()
		if default:
			set_widget_value(input_widget, default)

	field_layout = w.QVBoxLayout()
	field_layout.addWidget(label_widget)
	field_layout.addWidget(input_widget)
	field_layout.addWidget(error_widget)
	
	
	return label_widget, input_widget, error_widget, field_layout
