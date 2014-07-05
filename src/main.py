from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QFileDialog
from git.Commit import Commit
import logging
import os
import sys
from PyQt4 import QtGui
from canvas.GGraphicsScene import GGraphicsScene
from git.LocalRepository import LocalRepository
from mainwindow import Ui_MainWindow


class VisualGit(QtGui.QMainWindow):
    """
    The main application window

    Attributes:
        open_repos: A map of absolute paths to open LocalRepositories_
    """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Load UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connect_signals_to_slots()

        # Initialize attributes
        self.open_repos = {}

    def _connect_signals_to_slots(self):
        """
        Connect all signals to their corresponding slots
        """

        # Connect action signals to their slots
        self.ui.action_open.triggered.connect(self._open_repo)

        # Connect all other signals to their slots
        self.ui.tabs_canvas.tabCloseRequested.connect(self._close_canvas_tab)

    @pyqtSlot()
    def _open_repo(self):
        """
        Prompt the user to select a local git repository to open
        """

        # Prompt the user to select a local repo with a file chooser dialog
        repo_path = QFileDialog.getExistingDirectory(self, "Open a Local Git Repository",
                                                     options=QFileDialog.ShowDirsOnly)
        # Open the selected local repo
        if repo_path:
            # If the selected repo is not already open
            if repo_path not in self.open_repos:
                # Get commit history and branches for selected repository
                repo = LocalRepository(repo_path)
                root_commit = repo.get_commit_graph()
                branches = repo.branches

                # Show the root commit's details by default
                self._show_commit_details(root_commit)

                # Add selected repo to the set of open repos
                self.open_repos[repo_path] = repo

                # Add a new Canvas tab for the repo
                canvas = QtGui.QGraphicsView()
                canvas.repo_path = repo_path
                repo_name = repo_path.rsplit("/", 1)[1]
                index = self.ui.tabs_canvas.addTab(canvas, repo_name)
                self.ui.tabs_canvas.widget(index).setStatusTip(repo_path)

                # Display repo's commit graph on a new Canvas
                q_graphics_scene = GGraphicsScene()
                canvas.setScene(q_graphics_scene)
                q_graphics_scene.render_scene(root_commit, branches)
                self.ui.tabs_canvas.setCurrentWidget(canvas)

                # Setup signals for the Canvas
                q_graphics_scene.commitnode_selected.connect(self._show_commit_details)
            else:
                # Show existing tab containing selected repo
                for i in range(0, self.ui.tabs_canvas.count()):
                    if repo_path == self.ui.tabs_canvas.widget(i).repo_path:
                        self.ui.tabs_canvas.setCurrentIndex(i)

    @pyqtSlot(int)
    def _close_canvas_tab(self, index):
        """
        Close the Canvas tab at the given index and it's corresponding
        LocalRepository_
        """

        self.open_repos.pop(self.ui.tabs_canvas.widget(index).repo_path)
        self.ui.tabs_canvas.removeTab(index)

    @pyqtSlot(Commit)
    def _show_commit_details(self, commit):
        """
        Display the details of the given commit in the Commit Explorer

        :param commit: The Commit to display
        """

        self.ui.lbl_commit_msg_header.setText(commit.message.splitlines()[0])
        self.ui.txt_commit_sha.setText(commit.sha.name)
        self.ui.txt_author_name.setText(commit.author.name)
        self.ui.txt_author_email.setText(commit.author.email)
        self.ui.txt_author_date.setText(commit.date_authored.strftime("%x"))
        self.ui.txt_author_time.setText(commit.date_authored.strftime("%X"))
        self.ui.txt_committer_name.setText(commit.committer.name)
        self.ui.txt_committer_email.setText(commit.committer.email)
        self.ui.txt_commit_date.setText(commit.date_committed.strftime("%x"))
        self.ui.txt_commit_time.setText(commit.date_committed.strftime("%X"))
        self.ui.txt_commit_msg.setText(commit.message)


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
    win = VisualGit()
    win.show()

    # Exit will error code from app
    sys.exit(app.exec_())
