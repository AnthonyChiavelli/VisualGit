import logging
import os
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


def init_loggers():
    """
    Set up the loggers for use.

    Always call this before attempting a log statement. Failure to do
    so will result in a new, uninitialized logger being created without
    the desired behavior of these loggers.

    This function provides two loggers: 'app_logger', for logging
    program information to the console, and 'git_interaction_logger',
    for logging all git interactions made by the user to a log file
    located in the /logs directory of the project root.

    Instances of these loggers can be acquired by calling
    logging.getLogger() and passing in the name of the desired logger.

    The log level for both loggers is INFO
    """

    # Provides global application logging to stderr
    app_logger = logging.getLogger('app_logger')
    app_logger.setLevel(logging.INFO)
    app_logger_handler = logging.StreamHandler()
    app_logger_handler.setLevel(logging.INFO)
    app_logger_format = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    # Connect channel, logger, and formatter
    app_logger_handler.setFormatter(app_logger_format)
    app_logger.addHandler(app_logger_handler)

    # Provides logging of git user interactions to a file
    git_interaction_logger = logging.getLogger('git_interaction_logger')
    git_interaction_logger.setLevel(logging.INFO)
    git_interaction_log_dir = os.path.join(os.path.curdir, 'logs')
    # Create the log directory if it does not exist
    if not os.path.exists(git_interaction_log_dir):
        os.makedirs(git_interaction_log_dir)
        if not os.path.exists(git_interaction_log_dir):
            app_logger.error("log directory does not exist and cannot be created. Program will"
                             "precede without git interaction logging")
            return
    git_interaction_logger_handler = logging.FileHandler(
        os.path.join(git_interaction_log_dir, 'git_interaction_log'))
    git_interaction_logger_handler.setLevel(logging.INFO)
    git_interaction_logger_format = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s')
    # Connect channel, logger, and formatter
    git_interaction_logger_handler.setFormatter(git_interaction_logger_format)
    git_interaction_logger.addHandler(git_interaction_logger_handler)


def test_func():
    win.ui.commitMessageTextEdit.setText('Message!')

if __name__ == "__main__":
    # Initialize our logger
    init_loggers()

    # Begin the qt application and main window
    app = QtGui.QApplication(sys.argv)
    win = TestApp()

    # Exit will error code from app
    sys.exit(app.exec_())
