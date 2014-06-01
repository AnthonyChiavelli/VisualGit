from git.Branch import Branch
from git.GitObject import GitObject


class HeadPointer():
    """
    A special pointer used by git to refer to the currently checked out
    branch or commit

    Attributes:
        NAME: "HEAD"
        commit_sha: The Sha1 of the commit this HEAD pointer is referencing
    """

    NAME = "HEAD"

    def __init__(self, commit_sha):
        """Constructor"""
        self.commit_sha = commit_sha

    def __str__(self):
        """
        Return a string representation of this HEAD pointer
        """
        return "{0}({1})".format(self.__class__.__name__, self.commit_sha)

    def __eq__(self, other):
        """
        Return true if this HEAD pointer refers to the same commit as
        the other

        :param other: The HeadPointer to compare this to
        """
        if isinstance(other, (HeadPointer, Branch)):
            return self.commit_sha == other.commit_sha
        elif isinstance(other, GitObject):
            return self.commit_sha == other.sha
        else:
            return NotImplemented

    def __ne__(self, other):
        """
        Return true if this HEAD pointer refers to a different commit
        than the other

        :param other: The HeadPointer to compare this to
        """
        if isinstance(other, (HeadPointer, Branch)):
            return self.commit_sha != other.commit_sha
        elif isinstance(other, GitObject):
            return self.commit_sha != other.sha
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.commit_sha)