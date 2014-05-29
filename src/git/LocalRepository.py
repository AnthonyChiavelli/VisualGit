import logging
import os
import zlib
import sys

from git.Branch import Branch
from git.Commit import Commit
from git.GitObject import GitObject
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


class LocalRepository():
    """
    All files and file history associated with git are stored in the
    git directory (or local repository) for a project.

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
        """Constructor."""
        self.path = path
        self.rootcommit = None
        self.branches = []
        self.tags = []
        self.commits = {}

    def get_local_branch(self, branch_name):
        """
        Return the local Branch with the given name.

        :param branch_name: The name of the branch to be retrieved.
        """
        # Get the SHA-1 of the commit the given branch points to
        branch_file_contents = open(
            self.path + PATH_TO_BRANCHES + "/" + branch_name).read()
        branch = Branch(branch_name, Sha1(branch_file_contents))
        logger.debug("Found a local branch " + branch.name + " pointing to commit " +
                     str(branch.commit_sha)[:8])

        return branch

    def get_all_local_branches(self):
        """
        Return a list of all local Branches.
        """
        branchlist = []
        for branch_filename in os.listdir(self.path + PATH_TO_BRANCHES):
            branch = self.get_local_branch(branch_filename)
            branchlist.append(branch)
        return branchlist

    def get_git_object_contents(self, git_obj_sha):
        """
         Return the decompressed contents of the git object with the
         given SHA-1.

        :param git_obj_sha: The SHA-1 hash of the git object to be
            fetched.
        """

        git_obj = GitObject(git_obj_sha)
        git_obj_contents = open(self.path + PATH_TO_GIT_OBJECTS +
                                git_obj.get_subdirectory_name() + "/" +
                                git_obj.get_file_name(), "rb").read()
        git_obj_contents = zlib.decompress(git_obj_contents).decode()
        logger.debug("Git object " + str(git_obj_sha)[:8] + " contents:\n" + git_obj_contents)
        return git_obj_contents

    def get_commit_object(self, commit_sha):
        """
        Deserialize the commit object file contents.

        Commit object file contents are in the form::

            tree 2bddce7d093dfc7ce7911b5e8ae4ccbdf048b7d3
            parent a6407f4a8a2bef57ed84d4853a89e940f2834c11
            parent db5920fe02784ac83b2fe829a172383bb48c3027
            author Kahmali Rose <kahmali@mail.com> 1400873968 -0400
            committer Kahmali Rose <kahmali@mail.com> 1400924303 -0400

            Commit message begins after a blank line.


        :param commit_sha: The SHA-1 hash of the commit object to
            retrieve.
        :return The CommitObject with the given SHA-1.
        """

        # Get the decompressed contents of the commit object file
        commit_obj_file_contents = self.get_git_object_contents(commit_sha)

        # Deserialize the contents of the commit file
        commit = Commit(commit_sha)
        commit_message = ""
        reading_commit_message = False
        for line in commit_obj_file_contents.splitlines(True):
            if reading_commit_message:
                commit_message += str(line)
            else:
                if line is not EMPTY_LINE:
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
                        commit.commit_date = date_committed
                else:
                    # An empty line signifies the commit message is about to begin
                    reading_commit_message = True
        # Add the message to the commit
        commit.message = commit_message

        return commit

    def get_commit_history(self, commit_sha, child_commit=None):
        """
        Assemble the commit history for the commit with the given SHA-1.

        :param child_commit: The child we got to this commit from, if
            any. This is used to allow linking in both directions (from
            parent to child).
        """

        # Get the commit object with the given SHA-1
        current_commit = self.get_commit_object(commit_sha)
        self.commits[str(current_commit.sha)] = current_commit
        logger.debug("Getting history for commit " + str(current_commit.sha)[:8])

        # Add the given child, if any, to the current commit
        if child_commit is not None:
            current_commit.add_child(child_commit)
            logger.debug("Added child commit " + str(child_commit.sha)[:8] + " to commit " +
                         str(current_commit.sha)[:8])

        # Get the commit history for each parent
        if current_commit.parents:
            for parent in current_commit.parents:
                if str(parent.sha) not in self.commits:
                    self.get_commit_history(parent.sha, current_commit)
        else:
            # Current commit is the root
            self.rootcommit = current_commit
            logger.debug("Found root commit " + str(self.rootcommit.sha)[:8])

    def get_commit_graph(self):
        """
        Assemble and return the complete commit history for this local
        repository.

        :return The CommitObject at the root of the commit graph.
        """

        # Get a list of all the local branches
        self.branches = self.get_all_local_branches()

        # Assemble the commit history of each branch into a single (root) commit
        self.rootcommit = None
        self.commits = {}
        for branch in self.branches:
            if str(branch.commit_sha) not in self.commits:
                logger.debug("Getting commit history for branch " + branch.name + " at commit " +
                             str(branch.commit_sha)[:8])
                self.get_commit_history(branch.commit_sha)

        return self.rootcommit