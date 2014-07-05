from git.GitObject import GitObject


class Commit(GitObject):
    """
    A single node in a repository's history

    A commit is a set of changes, or patch, that is applied to a
    repository. This node contains only the history information,
    excluding any data concerning the actual project content contained
    in that commit.

    Attributes:
        parents: A list of Commits immediately preceding this one,
            historically. A Commit has one or more parents, unless it
            is the root (initial) commit, which has none.
        children: A list of Commits immediately following this one. A
            commit can have zero or more children.
        author: The GitUser that originally created this commit.
        committer: The GitUser that last applied this commit.
        date_authored: The date and time this commit was originally
            created.
        date_committed: The date and time this commit was last applied.
        message: A string typically containing a description of the
            changes made since the last commit. The common formatting
            convention is "50/72," named after the 50 character limit
            for the first (summary) line, and the 72 character limit
            for all additional lines.
    """

    def __init__(self, sha):
        """Constructor."""
        GitObject.__init__(self, sha)
        self.parents = []
        self.children = []
        self.author = None
        self.date_authored = None
        self.committer = None
        self.date_committed = None
        self.message = None

    def add_parent(self, parent_commit):
        """
        Add the given commit to the list of parents for this commit

        :param parent_commit: A commit that directly preceded this one
        """
        self.parents.append(parent_commit)

    def add_child(self, child_commit):
        """
        Add the given commit to the list of children for this commit

        :param child_commit: A commit that directly followed this one
        """
        self.children.append(child_commit)

    def __eq__(self, other):
        """
        Return True if this commit has the same SHA-1 hash as the other

        :param other: The Commit to compare this to
        """
        if isinstance(other, Commit):
            return self.sha == other.sha
        else:
            return NotImplemented

    def __ne__(self, other):
        """
        Return True if this commit has a different SHA-1 hash as the other

        :param other: The commit to compare this to
        """
        if isinstance(other, Commit):
            return self.sha != other.sha
        else:
            return NotImplemented

    def __gt__(self, other):
        """
        Return True if this commit came after the other,
            chronologically

        :param other: The commit to compare this to
        """
        return self.date_committed > other.date_committed

    def __ge__(self, other):
        """
        Return True if this commit came after or at the same time as
        the other

        :param other: The commit to compare this to
        """
        return self.date_committed >= other.date_committed

    def __lt__(self, other):
        """
        Return True if this commit came before the other,
            chronologically

        :param other: The commit to compare this to
        """
        return self.date_committed < other.date_committed

    def __le__(self, other):
        """
        Return True if this commit came before or at the same time as
        the other

        :param other: The commit to compare this to
        """
        return self.date_committed <= other.date_committed

    def __hash__(self):
        return hash(self.sha)