from .form import Form
from .validators import *
from .widgets import QIntegerEdit
from PyQt5 import QtWidgets as w


class CreateProductForm(Form):
    
    fields = {
        "name": {
            "label": "Product Name",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
        },
        "brand": {
            "label": "Brand Name",
            "data_type": str,
            "validators": [],
            "data_processor": None,
            "widget": w.QLineEdit,
        },
        "description": {
            "label": "Description",
            "data_type": str,
            "validators": [],
            "data_processor": None,
            "widget": w.QTextEdit
        },
        "barcode": {
            "label": "Barcode",
            "data_type": int,
            "validators": [RangeLen(max_len=10)],
            "data_processor": None,
            "widget": QIntegerEdit
        },
        "buying_price": {
            "label": "Cost Price",
            "data_type": int,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QIntegerEdit,
        },
        "selling_price": {
            "label": "Sell Price",
            "data_type": int,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QIntegerEdit,
        },
        "units": {
            "label": "Units",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
        }
    }


class UpdateProductForm(Form):

    fields = {
        "name": {
            "label": "Product Name",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
        },
        "brand": {
            "label": "Brand Name",
            "data_type": str,
            "validators": [],
            "data_processor": None,
            "widget": w.QLineEdit,
        },
        "description": {
            "label": "Description",
            "data_type": str,
            "validators": [],
            "data_processor": None,
            "widget": w.QTextEdit
        },
        "barcode": {
            "label": "Barcode",
            "data_type": int,
            "validators": [RangeLen(max_len=10)],
            "data_processor": None,
            "widget": QIntegerEdit
        },
        "buying_price": {
            "label": "Cost Price",
            "data_type": int,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QIntegerEdit,
        },
        "selling_price": {
            "label": "Sell Price",
            "data_type": int,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QIntegerEdit,
        },
        "units": {
            "label": "Units",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
        }
    }