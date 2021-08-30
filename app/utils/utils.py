from datetime import datetime


def combine_styles(style_list):
    style = ""
    for each in style_list:
        style += each
    return style


def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def comma_separator(value):
    if isinstance(value, int):
        return f'{value:,}'
    return value


def format_from_iso_date(iso_date, format='%d/%m/%Y %H:%M'):
    return datetime.strftime(datetime.strptime(iso_date, '%Y-%m-%d %H:%M:%S.%f'), format)


def render_list(string_list):
    output = "<ul>"
    for string in string_list:
        output += f"<li>{string}</li>"
    return output + "</ul"
