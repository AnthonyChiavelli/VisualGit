"""
The API for direct interaction with a local git repository.

When a git repository is initialized in a directory (using the git init
command), a .git directory is created there, and all files associated
with git are stored there. This API provides an interface for accessing
the information stored in those files, such as the local branches,
tags, and commit history.
"""
from logging import Logger
import logging
import os
import zlib
from model.Branch import Branch
from model.GitObject import GitObject
from model.Sha1 import Sha1


PATH_TO_BRANCHES = "/.git/refs/heads/"
PATH_TO_GIT_OBJECTS = "/.git/objects/"


def get_local_branch(path_to_git_directory, branch_name):
    """
    Returns a local branch with the given name from the given
    repository.

    :param path_to_git_directory: The absolute path to a local
        repository
    :param branch_name: The name of the branch to be retrieved
    :return The local branch with the given name
    """
    # Get the SHA-1 of the commit the given branch points to
    branch_file_contents = open(path_to_git_directory + PATH_TO_BRANCHES + "/" + branch_name).read()
    branch = Branch(branch_name, Sha1(branch_file_contents))
    # Logger.debug("Found a local branch " + branch.name + "pointing to commit " +
    #       branch.commitSha.get_string_of_length(8))

    return branch


def get_all_local_branches(path_to_git_directory):
    """
    Returns a list of local branches in the given repository.

    :param path_to_git_directory: The absolute path to a local
        repository
    :return A list of local branches from the given repository
    """
    branch_list = []
    for branch_file_name in os.listdir(path_to_git_directory + PATH_TO_BRANCHES):
        branch = get_local_branch(path_to_git_directory, branch_file_name)
        branch_list.append(branch)
        # logger = logging.getLogger()
        print("Found a local branch " + branch.name + " pointing to commit " +
              branch.commit_sha.get_string_of_length(8))
        print(get_git_object_contents(path_to_git_directory, branch.commit_sha))
    return branch_list


def get_git_object_contents(path_to_git_directory, git_obj_sha):
    """
     Returns the unzipped contents of the git object with the given
     SHA-1.

    :param path_to_git_directory: The absolute path to a local
        repository
    :param git_obj_sha: The SHA-1 hash of the git object to be
        fetched
    """

    git_obj = GitObject(git_obj_sha)
    git_obj_contents = open(path_to_git_directory + PATH_TO_GIT_OBJECTS +
                            git_obj.get_subdirectory_name() + "/" +
                            git_obj.get_file_name(), "rb").read()
    return zlib.decompress(git_obj_contents)


def _parse_commit_object(commit_object, commit_file_contents, commits_encountered):
    """
    Parses the commit object

    :param commit_object:
    :param commit_file_contents:
    :param commits_encountered:
    """


def get_commit_history(path_to_git_directory):
    """
    Returns the complete commit history for the local repository at the
    given path.

    :param path_to_git_directory:
    """

    # Create map for storing a record of all commits encountered (to prevent duplication)
    commits_encountered = {}

    # Get a list of all the local branches
    branches = get_all_local_branches(path_to_git_directory)

    # Assemble the commit history of each branch into a single CommitNode