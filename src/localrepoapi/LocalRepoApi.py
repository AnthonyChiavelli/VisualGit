"""
The API for direct interaction with a local git repository.

When a git repository is initialized in a directory (using the git init
command), a .git directory is created there, and all files associated
with git are stored there. This API provides an interface for accessing
the information stored in those files, such as the local branches,
tags, and commit history.
"""
import logging
import os
import zlib
import sys

from model.Branch import Branch
from model.CommitObject import CommitObject
from model.GitObject import GitObject
from model.Sha1 import Sha1


PATH_TO_BRANCHES = "/.git/refs/heads/"
PATH_TO_GIT_OBJECTS = "/.git/objects/"
EMPTY_LINE = "\n"

_root_commit = None

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_local_branch(path_to_local_repo, branch_name):
    """
    Returns a local branch with the given name from the given
    repository.

    :param path_to_local_repo: The absolute path to a local
        repository
    :param branch_name: The name of the branch to be retrieved
    :return The local branch with the given name
    """
    # Get the SHA-1 of the commit the given branch points to
    branch_file_contents = open(path_to_local_repo + PATH_TO_BRANCHES + "/" + branch_name).read()
    branch = Branch(branch_name, Sha1(branch_file_contents))
    logger.debug("Found a local branch " + branch.name + " pointing to commit " +
                 str(branch.commit_sha)[:8])

    return branch


def get_all_local_branches(path_to_local_repo):
    """
    Returns a list of local branches in the given repository.

    :param path_to_local_repo: The absolute path to a local
        repository
    :return A list of local branches from the given repository
    """
    branch_list = []
    for branch_file_name in os.listdir(path_to_local_repo + PATH_TO_BRANCHES):
        branch = get_local_branch(path_to_local_repo, branch_file_name)
        branch_list.append(branch)
    return branch_list


def get_git_object_contents(path_to_local_repo, git_obj_sha):
    """
     Returns the decompressed contents of the git object with the given
     SHA-1.

    :param path_to_local_repo: The absolute path to a local
        repository
    :param git_obj_sha: The SHA-1 hash of the git object to be
        fetched
    """

    git_obj = GitObject(git_obj_sha)
    git_obj_contents = open(path_to_local_repo + PATH_TO_GIT_OBJECTS +
                            git_obj.get_subdirectory_name() + "/" +
                            git_obj.get_file_name(), "rb").read()
    git_obj_contents = zlib.decompress(git_obj_contents).decode()
    logger.debug("Git object " + str(git_obj_sha)[:8] + " contents:\n" + git_obj_contents)
    return git_obj_contents


def get_commit_object(path_to_local_repo, commit_sha, commits_encountered):
    """
    Deserializes the commit object file contents.

    Commit object file contents are in the form::

        tree 2bddce7d093dfc7ce7911b5e8ae4ccbdf048b7d3
        parent a6407f4a8a2bef57ed84d4853a89e940f2834c11
        parent db5920fe02784ac83b2fe829a172383bb48c3027
        author Kahmali Rose <kahmali@mail.com> 1400873968 -0400
        committer Kahmali Rose <kahmali@mail.com> 1400924303 -0400

        Commit message begins after a blank line.


    :param path_to_local_repo: The absolute path to the local repo
        where the commit object is stored
    :param commit_sha: The SHA-1 hash of the commit object to retrieve
    :param commits_encountered: A list of the commits encountered on
        the latest search of the repo history
    """

    # Get the decompressed contents of the commit object file
    commit_obj_file_contents = get_git_object_contents(path_to_local_repo, commit_sha)

    # Deserialize the contents of the commit file
    commit = CommitObject(commit_sha)
    commit_message = ""
    reading_commit_message = False
    for line in commit_obj_file_contents.splitlines(True):
        if reading_commit_message:
            commit_message += str(line)
        else:
            if line is not EMPTY_LINE:
                # Get the details about the commit
                split_line = line.split()
                keyword = split_line[0]
                if keyword == "parent":
                    # Add a parent to the commit
                    parent_sha_str = split_line[1]
                    if parent_sha_str in commits_encountered:
                        # Link the current commit with it's existing parent commit
                        commits_encountered[parent_sha_str].add_child(commit)
                        commit.add_parent(commits_encountered[parent_sha_str])
                    else:
                        # Add a new commit object as the parent of the current commit
                        commit.add_parent(CommitObject(Sha1(parent_sha_str)))
            else:
                # An empty line signifies the commit message is about to begin
                reading_commit_message = True
    # Add the message to the commit
    commit.message = commit_message

    return commit


def get_commit_history(path_to_local_repo, commit_sha, commits_encountered, child_commit=None):
    """
    Returns the commit history for the commit with the given SHA-1 if
    it hasn't already been encountered.

    :param path_to_local_repo: The local repository the commit belongs
        to
    :param commit_sha: The SHA-1 hash of the commit to get the history
        for
    :param commits_encountered: A map of SHA-1's to CommitObjects that
        have already been encountered
    :param child_commit: The child we got to this commit from, if any.
        This is used to allow linking in both directions (from parent
        to child).
    """

    global _root_commit

    # Get the commit object with the given SHA-1
    current_commit = get_commit_object(path_to_local_repo, commit_sha, commits_encountered)
    commits_encountered[str(current_commit.sha)] = current_commit
    logger.debug("Getting history for commit " + str(current_commit.sha)[:8])

    # Add the given child, if any, to the current commit
    if child_commit is not None:
        current_commit.add_child(child_commit)
        logger.debug("Added child commit " + str(child_commit.sha)[:8] + " to commit " +
                     str(current_commit.sha)[:8])

    # Get the commit history for each parent
    if current_commit.parents:
        for parent in current_commit.parents:
            if str(parent.sha) not in commits_encountered:
                get_commit_history(path_to_local_repo, parent.sha, commits_encountered,
                                   current_commit)
    else:
        # Current commit is the root
        _root_commit = current_commit
        logger.debug("Found root commit " + str(_root_commit.sha)[:8])


def get_git_graph(path_to_local_repo):
    """
    Returns the complete commit history for the local repository at the
    given path.

    :param path_to_local_repo: The absolute path to a local repo
    """

    global _root_commit

    # Get a list of all the local branches
    branches = get_all_local_branches(path_to_local_repo)

    # Assemble the commit history of each branch into a single (root) commit
    _root_commit = None
    commits_encountered = {}
    for branch in branches:
        if str(branch.commit_sha) not in commits_encountered:
            logger.debug("Getting commit history for branch " + branch.name + " at commit " +
                         str(branch.commit_sha)[:8])
            get_commit_history(path_to_local_repo, branch.commit_sha, commits_encountered)

    return _root_commit