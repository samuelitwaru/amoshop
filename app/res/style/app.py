
open_bracket = '{'
close_bracket = '}'

widget_style = f"""
{open_bracket}
background-color: #ffffff;
{close_bracket}
"""

button_style = f"""
{open_bracket}
background-color: blue; 
padding: 8px;
font: 16px;
{close_bracket}
"""

input_style = f"""
{open_bracket}
background-color: #ffffffee;
padding: 8px;
font: 16px;
{close_bracket}
"""


text_style = f"""
{open_bracket}
padding: 1px;
font: 14px;
{close_bracket}
"""

style = """
/* Customize any plain widget that is a child of a QMainWindow. */
QWidget {
    background-color: #fbf9f9;
}


/* mainFrame won't have this border-image since we have
   explicitly set it to 'none' using a more specific selector. */
QFrame, QLineEdit, QComboBox[editable="true"], QSpinBox {
    background: white;
    border-image: url(:/images/frame.png) 4;
    border-width: 3;
}

QLabel {
    border: none;
    border-image: none;
    padding: 0;
    background: none;
}



"""


card = """

"""

