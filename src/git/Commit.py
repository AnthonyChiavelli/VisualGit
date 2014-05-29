from git.GitObject import GitObject


class Commit(GitObject):
    """
    A single node in a repository's history.

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
        author_date: The date and time this commit was originally
            created.
        commit_date: The date and time this commit was last applied.
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
        self.author_date = None
        self.committer = None
        self.commit_date = None
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