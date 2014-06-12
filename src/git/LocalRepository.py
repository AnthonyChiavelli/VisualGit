import binascii
import glob
import logging
import os
import sys
import zlib

from git.Branch import Branch
from git.Commit import Commit
from git.GitObject import GitObject
from git.GitTerminal import GitTerminal
from git.GitUser import GitUser
from git.Sha1 import Sha1
from datetime import datetime
from profilehooks import profile

PATH_TO_BRANCHES = ".git/refs/heads/"
PATH_TO_GIT_OBJECTS = ".git/objects/"
PATH_TO_PACKFILES = ".git/objects/pack/"

app_logger = logging.getLogger()
app_logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
app_logger.addHandler(ch)


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
        commits: A map of SHA-1 hash strings to the CommitObjects they
            identify in this repository.
    """

    def __init__(self, path):
        """Constructor"""
        self.path = path
        self.rootcommit = None
        self.branches = []
        self.commits = {}

    @profile
    def get_commit_graph(self):
        """
        Assemble and return the complete commit history for this local
        repository

        The commit history in a git repository is a directed acyclic
        graph, and can always be traced back to a root node, which is
        the first commit after a repository is initialized. This is the
        commit that gets returned, and it contains, via it's children,
        the complete commit history in this local repository.

        :return The Commit_ at the root of the commit graph
        """

        # A stack of "empty" commits (only containing SHA-1s) that we need to get complete info for
        commit_stack = []

        # Assemble the commit history for each local branch
        self.branches = self._get_all_local_branches()
        for branch in self.branches:
            # Add the branch's (empty) commit to the stack if we haven't already encountered it
            if branch.commit_sha.name not in self.commits:
                commit_stack.append(Commit(branch.commit_sha))
                # Get complete details for each commit in the branch's history
                while commit_stack:
                    # Get a Commit off the stack and add it to the list of commits we've encountered
                    current_commit = commit_stack.pop()
                    self.commits[current_commit.sha.name] = current_commit

                    # Get complete details for the commit
                    current_commit = self._get_commit_object(current_commit)
                    app_logger.debug("Getting history for commit {0}"
                                     .format(current_commit.sha[:8]))

                    if current_commit.parents:
                        # Place each parent on the stack if we haven't encountered it before
                        for parent in current_commit.parents:
                            if parent.sha.name not in self.commits:
                                commit_stack.append(parent)
                    else:
                        # This commit is the root of this git graph
                        self.rootcommit = current_commit
                        app_logger.debug("Found root commit {0}".format(self.rootcommit.sha[:8]))

        # Log the number of commits found and the root commit
        app_logger.debug("Found {0} commits with root commit {1}"
                         .format(str(len(self.commits)), self.rootcommit.sha[:8]))

        return self.rootcommit

    def _get_all_local_branches(self):
        """
        Return a list of all local branches in this repository
        """
        branches = []
        for branch_filename in os.listdir(os.path.join(self.path, PATH_TO_BRANCHES)):
            branch = self._get_local_branch(branch_filename)
            branches.append(branch)

        return branches

    def _get_local_branch(self, branch_name):
        """
        Return the local Branch with the given name

        :param branch_name: The name of the branch to be retrieved
        """
        # Get the SHA-1 of the commit the given branch points to (full contents of the branch file)
        branch_file = open(os.path.join(self.path, PATH_TO_BRANCHES, branch_name))
        branch_file_contents = branch_file.read()
        branch_file.close()

        # Create a Branch pointing to the commit with the SHA-1 we find
        branch = Branch(branch_name, Sha1(branch_file_contents))

        # Log the branch we found
        app_logger.debug("Found a local branch {0} pointing to commit {1}"
                         .format(branch.name, branch.commit_sha[:8]))

        return branch

    def _get_commit_object(self, commit):
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
        commit_obj_file_contents = self._get_git_object_contents(commit.sha)

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
                            commit.add_parent(self.commits[parent_sha_str])
                            self.commits[parent_sha_str].add_child(commit)
                        else:
                            # Link the current commit with a new parent commit
                            parent = Commit(Sha1(parent_sha_str))
                            commit.add_parent(parent)
                            parent.add_child(commit)
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

    def _get_git_object_contents(self, git_obj_sha):
        """
         Return the decompressed contents of the git object with the
         given SHA-1, or None if the object is not found

         Git objects are stored either loose or packed. Loose objects
         are stored in the .git/objects/ directory. They are organized
         into subdirectories with names corresponding to the first two
         characters of the SHA-1 IDs of git objects contained within
         them. The objects are stored in zlib-compressed files with
         names corresponding to the last 38 characters of the SHA-1 IDs
         of the git objects they represent.

         Git can further compress loose git objects into packfiles when
         a repository grows too large, or garbage collection is run.
         There are two files we care about in the pack: the pack index
         and the pack file. See the `Git Community Book by Scott Chacon <http://schacon.github.io/gitbook/7_the_packfile.html>`_
         or the `git documentation <http://repo.or.cz/w/git.git/blob_plain/HEAD:/Documentation/technical/pack-format.txt>`_
         for detailed information on the data format of packfiles.

        :param git_obj_sha: The SHA-1 hash of the git object to be
            fetched
        """

        git_obj_contents = None
        git_obj = GitObject(git_obj_sha)
        loose_obj_path = os.path.join(self.path, PATH_TO_GIT_OBJECTS,
                                      git_obj.get_subdirectory_name(), git_obj.get_file_name())

        # Get the decompressed contents of the git object with the given SHA-1
        if os.path.exists(loose_obj_path):
            # Object is loose, so just decompress it
            git_obj_file = open(os.path.join(self.path, PATH_TO_GIT_OBJECTS,
                                             git_obj.get_subdirectory_name(),
                                             git_obj.get_file_name()), "rb")
            git_obj_contents = git_obj_file.read()
            git_obj_contents = zlib.decompress(git_obj_contents).decode()
            git_obj_file.close()

            # Log the decompressed object
            app_logger.debug("Loose git object {0} contents:\n{1}"
                             .format(git_obj_sha[:8], git_obj_contents))
        elif os.path.exists(os.path.join(self.path, PATH_TO_PACKFILES)):
            # Check for the object in the pack file
            packfiles_path = os.path.join(self.path, PATH_TO_PACKFILES)
            packfile_name = glob.glob(packfiles_path + "*.pack")[0]
            packfile = open(packfile_name, "rb")

            # Get the packfile version number
            packfile.seek(4)
            packfile_version = int.from_bytes(packfile.read(4), byteorder="big")
            # Get the number of git objects in the packfile
            packfile_numobjects = int.from_bytes(packfile.read(4), byteorder="big")

            # Get the pack index file
            packindex_filename = glob.glob(packfiles_path + "*.idx")[0]
            packindex = open(packindex_filename, "rb")

            # Use the index fanout table to find the range within the sha/offset table to search
            lowerbound, upperbound = _get_fanout_range(git_obj_sha, packindex, packfile_version)

            # Find the offset of git object within the pack file, if it exists
            offset = _get_pack_offset_v2(git_obj_sha, packindex, lowerbound, upperbound,
                                         packfile_numobjects)

            if offset:  # Git object found in pack index
                # Unpack the git object at the given offset
                git_obj_contents = self._unpack_git_object_v2(packfile, offset, git_obj_sha)
                app_logger.debug("Packed git object {0} contents:\n{1}"
                                 .format(git_obj_sha[:8], git_obj_contents))
            else:   # Git object not found in pack index
                app_logger.error("Git object {0} not found".format(git_obj_sha[:10]))

            # Close packfiles
            packfile.close()
            packindex.close()
        else:   # Git object not found in git directory
            # Make a last ditch effort to find the object via command line
            git_terminal = GitTerminal(self.path)
            git_obj_contents = git_terminal.show_git_objects_contents(git_obj_sha)
            if git_obj_contents:
                # Log the decompressed object
                app_logger.debug("Loose git object {0} contents:\n{1}"
                                 .format(git_obj_sha[:8], git_obj_contents))
            else:   # Git object not found anywhere
                app_logger.error("Git object {0} not found".format(git_obj_sha[:10]))

        return git_obj_contents

    def _unpack_git_object_v2(self, packfile, offset, git_obj_sha):
        """
        Return the decompressed contents of the git object from the
        pack file

        :param packfile: The pack file for this local repo
        :param offset: The offset of the git object in the pack file, in number of bytes from the
            start of the file
        :param git_obj_sha: The Sha1_ of the git object we're looking for
        :return: A string with the decompressed contents of the git object
        """

        # Move the file cursor to the beginning of the packed git object
        packfile.seek(offset)

        # Scan past the object header
        while (int.from_bytes(packfile.read(1), byteorder="big") & 0x80) != 0:
            pass

        # TODO: Calculate the size of the compressed object (default to 2kb for now - over is okay)
        objsize = 2048
        # Decompress the git object contents
        try:
            objcontents = zlib.decompress(packfile.read(objsize)).decode()
        except (zlib.error, UnicodeDecodeError):
            git_term = GitTerminal(self.path)
            objcontents = git_term.show_git_objects_contents(git_obj_sha)

        return objcontents


def _get_fanout_range(git_obj_sha, packindex, packindex_version):
    """
    Return the range within the sha/offset table to search

    :param git_obj_sha: The Sha1_ of the git object to search for
    :param packindex: The pack index file to search
    :param packindex_version: The version of the pack index (currently 1 or 2)
    :return: A tuple with the lower and upper bound to search for the given git object in the
        pack index
    """

    if packindex_version == 1:
        fanout_start = 0
    else:
        fanout_start = 8
    sha_index = int(git_obj_sha[:2], 16)
    fanout_index = fanout_start + ((sha_index - 1) * 4)
    packindex.seek(fanout_index)
    # Set the lower bound to the value at fanout[sha_index - 1] (e.g., if sha_index = 0x3c,
    # the lower bound will be at fanout[0x3b])
    if sha_index != 0x00:
        lowerbound = int.from_bytes(packindex.read(4), byteorder="big")
    else:
        # Set the lower bound manually since there is no entry before fanout_table[0]
        lowerbound = 0
        packindex.seek(4, 1)
    # The upper bound is given by the value at fanout_table[sha_index]
    upperbound = int.from_bytes(packindex.read(4), byteorder="big")

    return lowerbound, upperbound


def _get_pack_offset_v2(git_obj_sha, packindex, low, high, size):
    """
    Return a tuple with the range of the given git object in the
    packfile (version 2), in bytes, or None if the object is not found

    Uses a binary search, so it is O(log n) on average, where n is
    the number of objects in the packfile with the same first two
    characters in their SHA-1 identifier.

    See the `Git Community Book by Scott Chacon<http://schacon.github.io/gitbook/7_the_packfile.html>`_ or the `git
    documentation<http://repo.or.cz/w/git.git/blob_plain/HEAD:/Documentation/technical/pack-format.txt>`_ for detailed information on the data format of
    packfiles.



    :param git_obj_sha: The Sha1_ identifier of the git object
        we're looking for
    :param packindex:
    :param low:
    :param high:
    :param size: The total number of git objects stored in the
        packfile
    """

    # Each entry in the sha table is a SHA-1 (20 bytes)
    sha_size = 20
    # Each entry in the offset table is a 4 byte integer
    offset_size = 4
    #  The sha table begins after the header (2 * 4 bytes) and fanout table (256 * 4 bytes)
    sha_table_start = 1032
    # The offset table begins after the sha table (size * 20 bytes) and the crc checksum table
    # (size * 4 bytes)
    offset_table_start = sha_table_start + (size * 24)

    # Use a binary search to find the sha and it's offset in the packfile
    while low <= high:
        mid = (low + high) // 2
        # Check the given sha against the sha at sha_table[mid]
        packindex.seek(sha_table_start + (mid * sha_size))
        mid_sha = Sha1(binascii.hexlify(packindex.read(sha_size)).decode())
        if mid_sha < git_obj_sha:
            low = mid + 1
        elif mid_sha > git_obj_sha:
            high = mid - 1
        else:   # We've found the matching sha
            # Get the offset of the object in the pack file at offset_table[mid]
            packindex.seek(offset_table_start + (mid * offset_size))
            return int.from_bytes(packindex.read(offset_size), byteorder="big")
    return None
