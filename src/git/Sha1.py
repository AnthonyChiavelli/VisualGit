class Sha1():
    """
    Represents a SHA-1 hash string used as an identifier for git
    objects.

    Although a SHA-1 contains 40 alphanumeric characters, typically,
    the first 5-7 characters are enough to use as a unique identifier
    within any git repository.
    """

    def __init__(self, hash_string):
        """
        Constructor.
        """
        self._hash_string = hash_string

    def __str__(self):
        """
        Returns the SHA-1 hash string

        """
        return self._hash_string

    def get_string_of_length(self, n):
        """
        Returns the first n characters from the hash string

        :param n: The length of the string needed
        """
        return self.hash_string[:n]

    @property
    def hash_string(self):
        """
        40-character SHA-1 hash string
        """
        return self._hash_string