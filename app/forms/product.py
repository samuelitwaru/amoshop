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
            "default": "Bread",
        },
        "brand": {
            "label": "Brand Name",
            "data_type": str,
            "validators": [],
            "data_processor": None,
            "widget": w.QLineEdit,
            "default": "Tip Top",
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
            "default": "4000",
        },
        "selling_price": {
            "label": "Sell Price",
            "data_type": int,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QIntegerEdit,
            "default": "5000",
        },
        "units": {
            "label": "Units",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
            "default": "Loaves",
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

    # def __init__(self, product, **kwargs):
    #     Form.__init__(Form, **kwargs)
    #     self.fields["name"]["default"] = product["name"]
    #     self.fields["brand"]["default"] = product["brand"]
    #     self.fields["description"]["default"] = product["description"]
    #     self.fields["barcode"]["default"] = product["barcode"]
    #     self.fields["buying_price"]["default"] = product["buying_price"]
    #     self.fields["selling_price"]["default"] = product["selling_price"]
    #     self.fields["units"]["default"] = product["units"]
