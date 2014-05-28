class Branch():
    """
    A reference to a commit.

    A branch points to one and only one commit at ay given moment.
    Local branches are stored in the local repository, in the
    .git/refs/heads directory. They are stored by name, with each
    file containing the SHA-1 hash of the commit the branch is
    pointing to.
    """

    def __init__(self, name, commit_sha):
        """
        Constructor.
        """
        self._name = name
        self._commit_sha = commit_sha

    @property
    def name(self):
        """
        The name of this branch
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the name of the branch to the given value
        """
        self._name = value

    @property
    def commit_sha(self):
        """
        The SHA-1 hash string of the commit this branch is pointing to
        """
        return self._commit_sha

    @commit_sha.setter
    def commit_sha(self, value):
        """
        Set the SHA-1 hash of the commit the branch is pointing at to
        the given value
        """
        self._commit_sha = value
