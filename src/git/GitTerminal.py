
import subprocess
from git.Sha1 import Sha1

SUCCESS = 0  # used to check if a command was executed successfully.


class GitTerminal:
    """
    Represents a git terminal where git commands can be executed
    as if they where being manually ran on the shell/terminal.

    The core of this class is the "execute_comand" method, which uses
    the python subprocess.popen library to execute commands through
    the shell.

    List of supported commands:

        COMMAND            OPTIONS        TODO
        * git init
        * git merge                       how to deal with merge conflicts?
        * git commit
        * git branch

    Attributes:
        path_to_local_repository: A string representing the
                                  absolute path to the git directory.
    """

    def __init__(self, path_to_local_repository):
        """Constructor"""
        self.path_to_local_repository = path_to_local_repository

    def git_init(self):
        """
        Initializes a git repo.

        Returns a boolean value representing whether a git command
        was successfully executed (True)
        or a failure happened (False).
        """
        command = "cd " + self.path_to_local_repository + ";git init"
        output = GitTerminal.execute_command(command)
        return output[0]

    def git_merge(self, list_of_branches):
        """
        Merges git Branches

        Returns a tuple containing:
                * a boolean value representing whether
                  a git command was successfully executed (True)
                  or a failure happened (False).

                * a string containing the output message from the git
                  command executed ("git merge").

        :param list_of_branches: contains branches to be merged
                                 together
        """

        # Grab the name of the branches to be merged together.
        branch_names = ""
        for branch in list_of_branches:
            branch_names += branch.name + " "

        command = "cd " + self.path_to_local_repository + ";git merge " + branch_names
        output = GitTerminal.execute_command(command)
        return output

    def git_commit(self, commit_message):
        """
        Commits/saves changes made to the git repository.

        Returns a boolean value representing whether a git command
        was successfully executed (True value)
        or a failure happened (False value).

        :param commit_message: a descriptive message containing
                               information about changes made.
        """
        command = "cd " + self.path_to_local_repository + ";git commit -m \"" + commit_message + "\""
        output = GitTerminal.execute_command(command)
        return output[1]

    def git_branch(self):
        """
        Returns a tuple containing:
                * a boolean value representing whether
                  a git command was successfully executed (True)
                  or a failure happened (False).

                * a string containing a list of branches
                  in a git repository.
        """
        command = "cd " + self.path_to_local_repository + ";git branch"
        output = GitTerminal.execute_command(command)
        return output

    def show_git_objects_contents(self, sha):
        """
        Returns a string containing the contents of compressed file
        stored by git. The contents of compressed git files can be displayed by running the git command:
        "git cat-file -p <sha1>"

        :par
        am sha: The SHA-1 hash of a git object.
        """
        command = "cd " + self.path_to_local_repository + ";git cat-file -p " + sha.name
        output = GitTerminal.execute_command(command)
        return output[1]

    @staticmethod
    def execute_command(command):
        """
        Executes a git command.

        Returns a tuple containing:
                * a boolean value representing whether
                  a git command was successfully executed (True)
                  or a failure happened (False).

                * a string containing the output message from the git
                  command executed.

        :param command: a string containing the absolute path to the
                        local repo and the git command to be executed.

        command to be executed are in the form:
            cd /home/username/dir/another_dir ; git init


        we use popen from the python subprocess library to execute
        a git command on the terminal.

        "shell=True" is necessary in order for popen to run a command
        passed in as a string other options like stdout=PIPE are
        necessary in order to grab the output of the command that was
        executed note that we redirect "stderr=STOUT", this way we
        treat errors as normal output.
        """
        command_line_process = subprocess.Popen(command,
                                                shell=True,
                                                universal_newlines=True,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.STDOUT,
                                                stdin=subprocess.PIPE)

        # verifies if it is safe to grab the output from a git command before we call ".communicate"
        # which will close the process. ".read" can not be called after the process is closed.
        while True:
            # returns None while subprocess is running.
            if command_line_process.poll() is None:
                break

        # read the output before closing the process.
        output = command_line_process.stdout.read()

        # closes the process.
        command_line_process.communicate()

        # check if the git command was executed properly
        if command_line_process.returncode == SUCCESS:
            return True, output  # tuple
        else:
            return False, output  # tuple