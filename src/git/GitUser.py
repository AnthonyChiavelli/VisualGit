class GitUser():
    """
    Identity of a git user: name and email address

    Used to log user actions on a git repository (e.g., committing).

    Attributes:
        name: A string identifying this user (either full or nickname).
        email: User's email address (format not verified).
    """

    def __init__(self, name="", email=""):
        """Constructor"""
        self.name = name
        self.email = email

    def __str__(self):
        """
        Return a string representation of this git user
        """
        return "GitUser(Name: {0}, Email: {1})".format(self.name, self.email)

    def __eq__(self, other):
        """
        Return True if this git user has the same name and email
        address as the other

        :param other: The GitUser to compare this to
        """
        if isinstance(other, GitUser):
            return self.name == other.name and self.email == other.email
        else:
            return NotImplemented

    def __ne__(self, other):
        """
        Return True if this git user has the same name and email
        address as the other

        :param other: The GitUser to compare this to
        """
        if isinstance(other, GitUser):
            return self.name != other.name or self.email != other.email
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.name, self.email))