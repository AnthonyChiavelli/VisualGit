import logging
import os
import zlib
import sys

from git.Branch import Branch
from git.Commit import Commit
from git.GitObject import GitObject
from git.GitTerminal import GitTerminal
from git.GitUser import GitUser
from git.Sha1 import Sha1
from datetime import datetime

PATH_TO_BRANCHES = "/.git/refs/heads/"
PATH_TO_GIT_OBJECTS = "/.git/objects/"
EMPTY_LINE = "\n"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

commit_count = 0


class LocalRepository():
    """
    .. _LocalRepository:

    All files and file history associated with git are stored in the
    git directory (or local repository) for a project

    When a git repository is initialized in a directory (using the git
    init command), a .git/ directory is created there, and all files
    associated with git are stored there. This class provides access to
    the information stored in those files, such as the local branches,
    tags, and commit history (a directed, acyclic graph of commits).

    Attributes:
        path: A string representing the absolute path to the git
            directory.
        rootcommit: A CommitObject at the root of the commit history,
            containing the complete commit history via it's children.
        branches: A list of all local Branches (references to commits)
            contained in this repository.
        tags: A list of all Tags (lightweight, annotated, and signed)
            contained in this repository.
        commits: A map of SHA-1 hash strings to the CommitObjects they
            identify in this repository.
    """

    def __init__(self, path):
        """Constructor"""
        self.path = path
        self.rootcommit = None
        self.branches = []
        self.tags = []
        self.commits = {}

    def get_commit_graph(self):
        """
        Assemble and return the complete commit history for this local
        repository

        :return The CommitObject at the root of the commit graph
        """

        global commit_count

        # Get a list of all the local branches
        self.branches = self.get_all_local_branches()

        # Get the Commit for each Branch and place it on a stack
        stack = []
        for branch in self.branches:
            if branch.commit_sha.name not in self.commits:
                stack.append(Commit(branch.commit_sha))
                # While the stack is not empty
                while stack:
                # Get a Commit off the stack
                    commit_count += 1
                    current_commit = stack.pop()
                    self.commits[current_commit.sha.name] = current_commit
                    current_commit = self.get_commit_object(current_commit)
                    logger.debug("Getting history for commit " + current_commit.sha[:8])
                    logger.debug("Commit count: " + str(commit_count))
                    # For each parent
                    if current_commit.parents:
                        for parent in current_commit.parents:
                            # If we haven't encountered the parent commit before
                            if parent.sha.name not in self.commits:
                                # link the popped Commit as the child and place the parent on stack
                                parent.add_child(current_commit)
                                stack.append(parent)
                    else:
                        self.rootcommit = current_commit
                        logger.debug("Found root commit " + self.rootcommit.sha[:8])

        return self.rootcommit

    def get_all_local_branches(self):
        """
        Return a list of all local branches
        """
        branchlist = []
        for branch_filename in os.listdir(self.path + PATH_TO_BRANCHES):
            branch = self.get_local_branch(branch_filename)
            branchlist.append(branch)

        return branchlist

    def get_local_branch(self, branch_name):
        """
        Return the local Branch with the given name

        :param branch_name: The name of the branch to be retrieved
        """
        # Get the SHA-1 of the commit the given branch points to
        branch_file_contents = open(
            self.path + PATH_TO_BRANCHES + "/" + branch_name).read()
        branch = Branch(branch_name, Sha1(branch_file_contents))
        logger.debug("Found a local branch " + branch.name + " pointing to commit " +
                     branch.commit_sha[:8])

        return branch

    def get_commit_object(self, commit):
        """
        Deserialize the given commit object file contents

        Commit object file contents are in the form::

            tree 2bddce7d093dfc7ce7911b5e8ae4ccbdf048b7d3
            parent a6407f4a8a2bef57ed84d4853a89e940f2834c11
            parent db5920fe02784ac83b2fe829a172383bb48c3027
            author Kahmali Rose <kahmali@mail.com> 1400873968 -0400
            committer Kahmali Rose <kahmali@mail.com> 1400924303 -0400

            Commit message begins after a blank line.


        :param commit: The commit object to retrieve
        :return The CommitObject with the given SHA-1
        """

        # Get the decompressed contents of the commit object file
        git_terminal = GitTerminal(self.path)
        commit_obj_file_contents = git_terminal.show_git_objects_contents(commit.sha)

        # Deserialize the contents of the commit file
        # commit = Commit(commit)
        commit_message = ""
        reading_commit_message = False
        for line in commit_obj_file_contents.splitlines(True):
            if reading_commit_message:
                commit_message += str(line)
            else:
                if not line.isspace():
                    # Get the details about the commit
                    words = line.split()
                    keyword = words[0]
                    if keyword == "parent":
                        # Add a parent to the commit
                        parent_sha_str = words[1]
                        if parent_sha_str in self.commits:
                            # Link the current commit with it's existing parent commit
                            self.commits[parent_sha_str].add_child(commit)
                            commit.add_parent(self.commits[parent_sha_str])
                        else:
                            # Add a new commit object as the parent of the current commit
                            commit.add_parent(Commit(Sha1(parent_sha_str)))
                    if keyword == "author":
                        # Get the author and date authored
                        author_name = " ".join(words[1:-3])
                        author_email = words[-3].strip("<>")
                        date_authored = datetime.fromtimestamp(int(words[-2]))
                        commit.author = GitUser(author_name, author_email)
                        commit.author_date = date_authored
                    if keyword == "committer":
                        # Get the committer and date committed
                        committer_name = " ".join(words[1:-3])
                        committer_email = words[-3].strip("<>")
                        date_committed = datetime.fromtimestamp(int(words[-2]))
                        commit.committer = GitUser(committer_name, committer_email)
                        commit.date_committed = date_committed
                else:
                    # An empty line signifies the commit message is about to begin
                    reading_commit_message = True
        # Add the message to the commit
        commit.message = commit_message

        return commit

    def get_git_object_contents(self, git_obj_sha):
        """
         Return the decompressed contents of the git object with the
         given SHA-1

        :param git_obj_sha: The SHA-1 hash of the git object to be
            fetched
        """

        git_obj = GitObject(git_obj_sha)
        git_obj_contents = open(self.path + PATH_TO_GIT_OBJECTS +
                                git_obj.get_subdirectory_name() + "/" +
                                git_obj.get_file_name(), "rb").read()
        git_obj_contents = zlib.decompress(git_obj_contents).decode()
        logger.debug("Git object " + git_obj_sha[:8] + " contents:\n" + git_obj_contents)

        return git_obj_contents