from git.GitObject import GitObject
from git.Tag import Tag


class AnnotatedTag(Tag):
    """
    A permanent reference to a commit, stored as an object in the git
    database

    Attributes:
        sha: The Sha1 identifier for this tag.
        tagger: The GitUser that created this tag.
        date_tagged: The date and time this tag was created.
        message: A string included with the tag. Typically used to
            describe changes since the previous tag (as tags are
            typically used for versioning).
    """

    def __init__(self, sha, name="", commit_sha=None, tagger=None, date_tagged=None, message=None):
        """Constructor"""
        Tag.__init__(self, name, commit_sha)
        self.sha = sha
        self.tagger = tagger
        self.date_tagged = date_tagged
        self.message = message