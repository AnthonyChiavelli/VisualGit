class Branch():
    """
    A reference to a commit

    A branch points to one and only one commit at ay given moment.
    Local branches are stored in the local repository, in the
    .git/refs/heads directory. They are stored by name, with each
    file containing the SHA-1 hash of the commit the branch is
    pointing to.

    Attributes:
        name: A string identifying this Branch.
        commit_sha: The Sha1 of the commit this branch is pointing to.
    """

    def __init__(self, name, commit_sha):
        """Constructor"""
        self.name = name
        self.commit_sha = commit_sha

    def __str__(self):
        """
        Return a string representation of this branch
        """
        return "Branch({0}: {1})".format(self.name, self.commit_sha)

    def __eq__(self, other):
        """
        Return true if this branch has the same name and points to the
        same commit as the other

        :param other: The Branch to compare this to
        """
        if isinstance(other, Branch):
            return self.name == other.name and self.commit_sha == other.commit_sha
        else:
            return NotImplemented

    def __ne__(self, other):
        """
        Return true if this branch has a different name or points to a
        different commit

        :param other: The Branch to compare this to
        """
        if isinstance(other, Branch):
            return self.name != other.name or self.commit_sha != other.commit_sha
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.name, self.commit_sha))