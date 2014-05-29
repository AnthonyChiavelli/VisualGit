class Tag():
    """
    A permanent, lightweight reference to a commit.

    Essentially, tags are a way to name a commit, and they are typically
    used to mark specific versions of a project.

    Attributes:
        name: A string identifying the tag (e.g., "v1.0").
        commit: The Sha1 of the commit referred to by this tag.
    """

    def __init__(self, name="", commit_sha=None):
        """Constructor."""
        self.name = name
        self.commit_sha = commit_sha

