from .form import Form
from .validators import *
from .widgets import QPasswordEdit, QSelect, QIntegerEdit
from PyQt5 import QtWidgets as w 


class LoginForm(Form):
    
    fields = {
        "username": {
            "label": "Username",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
        },
        "password": {
            "label": "Password",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QPasswordEdit,
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
        },
        "email": {
            "label": "Email",
            "data_type": str,
            "validators": [IsRequired(), Email()],
            "data_processor": None,
            "widget": w.QLineEdit,
        },
        "telephone": {
            "label": "Telephone",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QIntegerEdit,
        },
        "username": {
            "label": "Username",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
        },
        "password": {
            "label": "Password",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QPasswordEdit,
        },
        "confirm_password": {
            "label": "Confirm Password",
            "data_type": str,
            "validators": [EqualTo("password"), IsRequired()],
            "data_processor": None,
            "widget": QPasswordEdit,
        },

        "roles": {
            "label": "Roles",
            "data_type": list,
            "validators": [IsRequired()],
            "choices": {
                "admin": {"label": "Admin"},
                "cashier": {"label": "Cashier"},
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



class RegisterAsAdminForm(Form):
    
    fields = {
        "name": {
            "label": "Full Name",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
        },
        "email": {
            "label": "Email",
            "data_type": str,
            "validators": [IsRequired(), Email()],
            "data_processor": None,
            "widget": w.QLineEdit,
        },
        "telephone": {
            "label": "Telephone",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QIntegerEdit,
        },
        "username": {
            "label": "Username",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": w.QLineEdit,
        },
        "password": {
            "label": "Password",
            "data_type": str,
            "validators": [IsRequired()],
            "data_processor": None,
            "widget": QPasswordEdit,
        },
        "confirm_password": {
            "label": "Confirm Password",
            "data_type": str,
            "validators": [EqualTo("password"), IsRequired()],
            "data_processor": None,
            "widget": QPasswordEdit,
        },
        "roles": {
            "label": "Roles",
            "data_type": list,
            "validators": [IsRequired()],
            "choices": {
                "admin": {"label": "Admin", "checked": True},
            },
            "data_processor": None,
            "widget": QSelect,
        },
    }