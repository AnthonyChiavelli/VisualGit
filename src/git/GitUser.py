class GitUser():
    """
    Identity of a git user: name and email address.

    Used to log user actions on a git repository (e.g., committing).

    Attributes:
        name: A string identifying this user (either full or nickname).
        email: User's email address (format not verified).
    """

    def __init__(self, name="", email=""):
        """Constructor."""
        self.name = name
        self.email = email