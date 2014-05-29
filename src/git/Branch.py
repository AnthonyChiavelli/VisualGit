class Branch():
    """
    A reference to a commit.

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
        """Constructor."""
        self.name = name
        self.commit_sha = commit_sha
