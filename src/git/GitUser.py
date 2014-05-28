class GitUser():
    """
    Identity of a git user: name and email address.

    Used to log user actions on a git repository (e.g., committing).
    """

    def __init__(self, name="", email=""):
        """
        Constructor.
        """
        self._name = name
        self._email = email

    @property
    def name(self):
        """
        User's name (either full or nickname).
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        """
        User's email address (format not verified).
        """
        return self._email

    @email.setter
    def email(self, value):
        self._email = value