class Sha1():
    """
    Represents a SHA-1 hash string used as an identifier for git
    objects.

    Although a SHA-1 contains 40 alphanumeric characters, typically,
    the first 5-7 characters are enough to use as a unique identifier
    within any git repository.

    Attributes:
        name: A 40-character SHA-1 hash string.
    """

    def __init__(self, hash_string):
        """Constructor."""
        self.name = hash_string

    def __str__(self):
        """
        Return the string representation of this SHA-1 hash.
        """
        return self.name

    def get_string_of_length(self, n):
        """
        Return the first n characters from the hash string.

        :param n: The length of the string needed
        """
        return self.name[:n]