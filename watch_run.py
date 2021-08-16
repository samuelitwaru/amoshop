import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
from threading import Thread
import os
import subprocess


class MyThread(Thread):    

    def run(self):
        main_window.close()
        app.exec_()


class MyHandler(FileSystemEventHandler):
    pid = None
    def on_modified(self, event):
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

