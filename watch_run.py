import time
import pathlib
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
from threading import Thread
import os
import subprocess
from config import Config


def create_ui(ui_file):
    filename = ui_file.replace('.ui', '')
    print(f"Building UI File '{Config.UI_DIR}/{ui_file}'")
    os.system(f"pyuic5 --execute {Config.UI_DIR}/{ui_file} --output {Config.UI_DIR}/{filename}.py")


class MyHandler(FileSystemEventHandler):
    pid = None
    def on_modified(self, event):
        path = pathlib.Path(event.src_path)
        if path.suffix == '.ui':
            create_ui(path.name)
        if self.pid:
            os.system(f"kill {self.pid}")
        proc = subprocess.Popen(["python3", "run.py"])
        self.pid = proc.pid


proc = subprocess.Popen(["python3", "run.py"])
event_handler = MyHandler()
event_handler.pid = proc.pid
observer = Observer()
observer.schedule(event_handler, path=".", recursive=True)
observer.start()


try:
    while True:
        time.sleep(1)
except:
    observer.stop()

observer.join()

