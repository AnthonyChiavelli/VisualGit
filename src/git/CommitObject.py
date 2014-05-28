from git.GitObject import GitObject


class CommitObject(GitObject):
    """
    A single node in a repository's history.

    A commit is a set of changes, or patch, that is applied to a
    repository. This node contains only the history information,
    excluding any data concerning the actual project content contained
    in that commit.
    """

    def __init__(self, sha):
        """
        Constructor.
        """
        super(CommitObject, self).__init__(sha)
        self._parents = []
        self._children = []
        self._author = None
        self._author_date = None
        self._committer = None
        self._commit_date = None
        self._message = None

    def add_parent(self, parent_commit):
        """
        Adds the given commit to the list of parents for this commit

        :param parent_commit: A commit that directly preceded this one
        """
        self._parents.append(parent_commit)

    def add_child(self, child_commit):
        """
        Adds the given commit to the list of children for this commit

        :param child_commit: A commit that directly followed this one
        """
        self._children.append(child_commit)

    @property
    def parents(self):
        """
        The commits immediately preceding this one. A commit has one or
        more parents, unless it is the root (initial) commit, which has
        none.
        """
        return self._parents

    @property
    def children(self):
        """
        The commits immediately following this one. A commit can have
        zero or more children.
        """
        return self._children

    @property
    def author(self):
        """
        The git user that originally created this commit.
        """
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def author_date(self):
        """
        The date and time this commit was originally created.
        """
        return self._author_date

    @author_date.setter
    def author_date(self, value):
        self._author_date = value

    @property
    def committer(self):
        """
        The git user that last applied this commit.
        """
        return self._committer

    @committer.setter
    def committer(self, value):
        self._committer = value

    @property
    def commit_date(self):
        """
        The date and time this commit was last applied.
        """
        return self._commit_date

    @commit_date.setter
    def commit_date(self, value):
        self._commit_date = value

    @property
    def message(self):
        """
        The commit message typically contains a description of any
        changes made since the commit immediately preceding this one.
        """
        return self._message

    @message.setter
    def message(self, value):
        self._message = value