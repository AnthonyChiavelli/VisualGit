import sys

from PyQt4 import QtGui, QtCore, uic

from git.LocalRepository import LocalRepository

MAIN_UI_FILE = '/home/kahmali/Development/Projects/VisualGit/ui/mainwindow.ui'
TEST_REPOSITORY = '/home/kahmali/Development/Projects/TestGit'


class TestApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Load and display UI file
        self.ui = uic.loadUi(MAIN_UI_FILE)
        self.ui.show()

        # Connect testButton's clicked() signal to our testFunc() function
        self.connect(self.ui.testButton, QtCore.SIGNAL('clicked()'), test_func)

        # Test getting the commit history for a local repository
        test_repo = LocalRepository(TEST_REPOSITORY)
        root_commit = test_repo.get_commit_graph()


def test_func():
    win.ui.commitMessageTextEdit.setText('Message!')

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = TestApp()
    sys.exit(app.exec_())
