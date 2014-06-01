class Tag():
    """
    A permanent, lightweight reference to a commit

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

    def __str__(self):
        """
        Return a string representation of this tag
        """
        return "Tag({0}: {1})".format(self.name, self.commit_sha)

    def __eq__(self, other):
        """
        Return true if this tag has the same name and points to the
        same commit as the other

        :param other: The Tag to compare this to
        """
        if isinstance(other, Tag):
            return self.name == other.name and self.commit_sha == other.commit_sha
        else:
            return NotImplemented

    def __ne__(self, other):
        """
        Return true if this tag has a different name or points to a
        different commit than the other

        :param other: The Tag to compare this to
        """
        if isinstance(other, Tag):
            return self.name != other.name or self.commit_sha != other.commit_sha
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.name, self.commit_sha))

