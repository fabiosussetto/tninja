import os
import sys
import json

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

import subprocess

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

server_proc = None


class FileBrowser(QObject):

    def __init__(self, *args, **kwargs):
        self.main_window = kwargs.pop('main_window')
        super(FileBrowser, self).__init__(*args, **kwargs)

    @Slot()
    def select_dir(self):
        self._dirname = QFileDialog.getExistingDirectory(self.main_window,
            "Select project root", "~")

    def get_dirname(self):
        return self._dirname

    def set_dirname(self, value):
        self._dirname = value

    dirname = Property(str, get_dirname, set_dirname)


class ServerLogger(object):

    frame = None

    def __init__(self, frame):
        self.frame = frame

    def log(self, msg):
        script = 'server_logger.log("%s");' % msg
        self.frame.evaluateJavaScript(script)


class ServerController(QObject):

    def __init__(self, *args, **kwargs):
        self.app = kwargs.pop('main_window')
        super(ServerController, self).__init__(*args, **kwargs)


    @Slot(str)
    def start(self, options=None):
        global server_proc

        if isinstance(options, basestring):
            options = json.loads(options)

        options = options or {}

        default_options = {
            'port': 8005
        }

        options = dict(default_options, **options)

        cmd = ['python', os.path.join(BASE_DIR, 'server.py')]

        for key, val in options.items():
            cmd.extend(['--%s' % key, val])

        self.app.server_logger.log("Starting server...")
        server_proc = subprocess.Popen(cmd, cwd=BASE_DIR)
        self.app.server_logger.log("Server started on port %s." % options['port'])

    @Slot()
    def stop(self):
        self.app.server_logger.log("Stopping server...")
        if server_proc:
            server_proc.terminate()
            self.app.server_logger.log("Server stopped.")
        #print server_proc.wait()


class SettingsController(QObject):

    @Slot(str)
    def save(self, conf):
        print 'Conf', json.loads(conf)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        # Initialize the object as a QLabel
        super(MainWindow, self).__init__(parent)
        self.resize(650, 375)

        # self.setMinimumSize(550, 475)
        self.setWindowTitle('Templater')

        web_view = QWebView(parent)

        web_view.page().settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        self.server_logger = ServerLogger(web_view.page().mainFrame())

        self.server = ServerController(main_window=self)
        self.file_browser = FileBrowser(main_window=self)

        self.settings = SettingsController()

        web_view.load(QUrl("assets/index.html"))
        web_view.page().mainFrame().addToJavaScriptWindowObject('app_server', self.server)
        web_view.page().mainFrame().addToJavaScriptWindowObject('file_browser', self.file_browser)
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