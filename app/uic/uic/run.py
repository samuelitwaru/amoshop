import os


def create_ui(ui_file):
    filename = ui_file.replace('.ui', '')
    os.system(f"pyuic5 --execute {ui_file} --output {filename}.py")


def filter_ui_file(ui_file):
    if ui_file.endswith('.ui'):
        return ui_file


filtered = filter(filter_ui_file, os.listdir('.'))

for file in filtered:
    create_ui(file)