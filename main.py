import os
import sys
import json

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

import subprocess

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

server_proc = None

class ServerController(QObject):

    @Slot()
    def start(self):
        global server_proc
        base_project = os.path.join(BASE_DIR, 'project')
        cmd = ['python', os.path.join(BASE_DIR, 'server.py'), '--base_path', './project']
        server_proc = subprocess.Popen(cmd, cwd=BASE_DIR)

    @Slot()
    def stop(self):
        print "Stopping server"
        if server_proc:
            server_proc.terminate()
        #print server_proc.wait()


class SettingsController(QObject):

    @Slot(str)
    def save(self, conf):
        print 'Conf', json.loads(conf)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        # Initialize the object as a QLabel
        super(MainWindow, self).__init__(parent)
        self.resize(731, 475)

        self.setMinimumSize(400, 185)
        self.setWindowTitle('Dynamic Greeter')

        web_view = QWebView(parent)

        web_view.page().settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        self.server = ServerController()
        self.settings = SettingsController()

        web_view.load(QUrl("assets/index.html"))
        web_view.page().mainFrame().addToJavaScriptWindowObject('app_server', self.server)
        web_view.page().mainFrame().addToJavaScriptWindowObject('settings', self.settings)

        web_view.show()

        self.setCentralWidget(web_view)

    def closeEvent(self, event):
        self.server.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec_())