from .form import Form
from .validators import *
from .widgets import QPasswordEdit, QSelect
from PyQt5 import QtWidgets as w 


class LoginForm(Form):
    
    fields = {
        "username": {
            "label": "Username",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
            "default": "samit"
        },
        "password": {
            "label": "Email",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QPasswordEdit,
            "default": "123"
        },
    }


class CreateUserForm(Form):
    
    fields = {
        "name": {
            "label": "Full Name",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
            "default": "Okot Smith"
        },
        "email": {
            "label": "Email",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
            "default": "okotsmith@gmail.com"
        },
        "telephone": {
            "label": "Telephone",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
            "default": "077483822"
        },
        "username": {
            "label": "Username",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
            "default": "okotsmith"
        },
        "password": {
            "label": "Password",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QPasswordEdit,
            "default": "123"
        },
        "confirm_password": {
            "label": "Confirm Password",
            "data_type": str,
            "validators": [EqualTo("password"), IsRequired()],
            "data_processor": None,
            "widget": QPasswordEdit,
            "default": "123"
        },

        "roles": {
            "label": "Roles",
            "data_type": list,
            "validators": [IsRequired()],
            "choices": {
                "admin": {"label": "Admin"},
                "cashier": {"label": "Cashier", "checked":True},
            },
            "data_processor": None,
            "widget": QSelect,
        },
    }


class UpdateUserPasswordForm(Form):
    
    fields = {
        "current_password": {
            "label": "Current Password",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QPasswordEdit,
        },
        "new_password": {
            "label": "New Password",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QPasswordEdit,
        },
        "confirm_password": {
            "label": "Confirm Password",
            "data_type": str,
            "validators": [EqualTo("new_password", msg="Passwords do not match"), IsRequired()],
            "data_processor": None,
            "widget": QPasswordEdit
        },
    }