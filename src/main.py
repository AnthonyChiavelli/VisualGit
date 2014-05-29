import logging
import os
import sys
from PyQt4 import QtGui, uic
from canvas.GBranchLabel import GBranchLabel
from canvas.GCommitNode import GCommitNode
from canvas.GGraphicsScene import GGraphicsScene


class MainApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Load and display UI file
        self.ui = uic.loadUi('/home/anthony/dev/projects/VisualGit/ui/mainwindow.ui')

        # Add a graphics scene for the graphics view in our UI
        scene = GGraphicsScene()
        self.ui.graphicsView.setScene(scene)

        # Test shape
        ellipse = QtGui.QGraphicsEllipseItem()
        ellipse.setRect(0.0, 0.0, 20.0, 20.0)
        ellipse.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        scene.addItem(ellipse)

        # Test Commit node
        scene.addItem(GCommitNode())
        scene.addItem(GBranchLabel())

        self.ui.show()


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


if __name__ == "__main__":
    # Initialize our logger
    init_loggers()

    # Begin the qt application and main window
    app = QtGui.QApplication(sys.argv)
    win = MainApp()

    # Exit will error code from app
    sys.exit(app.exec_())