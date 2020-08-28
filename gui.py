from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.uic import *
import cpu1
from win10toast import ToastNotifier
from threading import *
import sys, os, subprocess, shutil
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import zipfile
import zlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        initt = 0

    def __init__(self, filepath):
        self.path = filepath

    def on_modified(self, event):
        toaster = ToastNotifier()
        toaster.show_toast("The " + self.path + " directory has been changed.",
                           "Visit the directory to see the modifications.", duration=5)


class FrontEnd(QDialog):
    def __init__(self):
        super(FrontEnd, self).__init__()
        loadUi('EAFrontEnd.ui', self)
        self.setStyleSheet("background:#eee")
        self.setWindowTitle('EA Security System')
        self.SelectFile.clicked.connect(self.cloud_thread)
        self.enable_btn.clicked.connect(lambda: Thread(target=self.enable_btn_select).start())
        self.history_btn.clicked.connect(self.history_btn_select)
        self.watchdog.clicked.connect(self.watchdog_threads)

    def watchdog_threads(self):
        try:
            filepath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            event_handler = MyHandler(filepath)
            observer = Observer()
            observer.schedule(event_handler, path=filepath, recursive=False)
            observer.start()
            t1 = Thread(target=self.enable_watchdog)
            t1.daemon = True
            t1.start()
        except Exception as error:
            return None

    def enable_watchdog(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def history_btn_select(self):
        try:
            t1 = Thread(target=self.history_thread)
            t1.start()
        except Exception as error:
            print(error)

    def history_thread(self):
        history_process = cpu1.get_processHistory()
        self.history_text.clearHistory()
        self.history_text.append(history_process)
        self.show()

    def enable_btn_select(self):
        self.enable_btn.setText("Enabled")
        toaster = ToastNotifier()
        toaster.show_toast("Ransomware Detection Activated", "Check the application for further security options",
                           duration=10)

        try:
            t1 = Thread(target=self.enable_btn_thread)
            t1.start()
        except Exception as error:
            print(error)

    def enable_btn_thread(self):
        cpu1.machine_learning()

    def cloud_thread(self):
        filePath = list(QFileDialog.getOpenFileNames(self, 'Select Files'))  # getting the selected files path

        i = []
        j = ''
        if (i in filePath) and (j in filePath):  # check if the selected files are empty.
            return None

        filePath = filePath[0]
        path = cpu1.get_drives() + 'Ranswomware Cloud Backup.zip'  # getting the path in order to save the zip_file temporarily
        compression = zipfile.ZIP_DEFLATED  # setting compression
        fantasy_zip = zipfile.ZipFile(path, 'w')  # creating zipfile
        i = 0
        while (i < len(filePath)):
            fantasy_zip.write(filePath[i], compress_type=compression)  # writing files to zipfile
            i = i + 1
        fantasy_zip.close()
        t1 = Thread(target=self.SelectFileFunction)
        # t1.daemon=True
        t1.start()
        t1.join()

    def SelectFileFunction(self):
        path = cpu1.get_drives() + 'Ranswomware Cloud Backup.zip'
        cpu1.upload(path)  # uploading the zipfile
        os.remove(path)  # deleting the zipfile from hard drive


def main():
    app = QApplication(sys.argv)
    widget = FrontEnd()
    widget.show()
    sys.exit(app.exec_())
    QCoreApplication.quit()


if __name__ == "__main__":
    main()
