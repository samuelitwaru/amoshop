from .utils import validator_in_validators, set_widget_value, render_widget
from .validators import IsRequired
from app.utils import render_list


class Form:

	def __init__(self, box_layout, form_data=dict(), return_func=None):
		self.form_data = form_data
		self.return_func = return_func
		self.form_data = dict()
		self.processed_data = dict()
		self.errors = dict()
		self.widgets = dict()
		self.layout = box_layout

	def validate_form_data(self):
		self.errors = dict()
		for field_name, field_props in self.fields.items():
			data = self.form_data[field_name]
			not_required = not validator_in_validators(IsRequired, field_props["validators"])
			for validator in field_props["validators"]:
				#  if data is not provided and not required, then dont validate
				#  else validate
				if not bool(data) and not_required:
					pass
				else:
					is_valid, data = validator.validate(self.form_data, data)
					if not is_valid:
						self.errors[field_name] = data
		
		if len(self.errors):
			return False
		return True

	def process_form_data(self):
		for field_name, field_props in self.fields.items():
			data = self.form_data[field_name]
			data_processor = self.fields[field_name].get("data_processor")
			if data_processor:
				data = data_processor(data)
			self.processed_data[field_name] = data
		return self.processed_data

	def layout_field_widgets(self):

		for key, value in self.fields.items():
			label_widget, input_widget, error_widget, field_layout = render_widget(value)
			if self.return_func:
				input_widget.returnPressed.connect(self.return_func)
			self.widgets[key] = {
				"label": label_widget,
				"input": input_widget,
				"error": error_widget,
				"layout": field_layout
			}
			self.layout.addLayout(field_layout)
		self.layout.addStretch()
		return self.widgets


	def show_errors(self):
		for key, value in self.form_data.items():
			error = self.errors.get(key, '')
			error_label = self.widgets[key]["error"]
			if error:
				if isinstance(error, list):
					error = render_list(error)
			error_label.setText(error)

	def clear(self):
		for key, value in self.form_data.items():
			error_label = self.widgets[key]["error"]
			input_widget = self.widgets[key]["input"]
			error_label.setText("")
			input_widget.clear()

	def set_widget_values(self):
		for field in self.widgets:
			input_widget = self.widgets[field]["input"]
			set_widget_value(input_widget, self.form_data.get(field, "") or "")

