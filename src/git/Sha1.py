class Sha1():
    """
    .. _Sha1:

    Represents a SHA-1 hash used as an identifier for git
    objects

    Although a SHA-1 contains 40 hexadecimal characters, typically,
    the first 5-8 characters are enough to use as a unique identifier
    within any git repository.

    Attributes:
        name: A 40-character SHA-1 hash string.
    """

    def __init__(self, hash_string):
        """Constructor"""
        self.name = hash_string

    def get_string_of_length(self, n):
        """
        Return the first n characters from the hash string

        :param n: The length of the string needed
        """
        return self.name[:n]

    def __getitem__(self, item):
        """
        Return the given character or substring
        :param item:
        :return:
        """
        return self.name[item]

    def __str__(self):
        """
        Return the string representation of this SHA-1 hash
        """
        return self.name

    def __gt__(self, other):
        """
        Return true if the hexadecimal value of this SHA-1 is greater
        than the other

        :param other: The SHA-1 hash to compare this to
        """
        return int(self.name, 16) > int(other.name, 16)

    def __lt__(self, other):
        """
        Return true if the hexadecimal value of this SHA-1 is less than
        the other

        :param other: The SHA-1 hash to compare this to
        """
        return int(self.name, 16) < int(other.name, 16)

    def __ge__(self, other):
        """
        Return true if the hexadecimal value of this SHA-1 is greater
        than or equal to the other

        :param other: The SHA-1 hash to compare this to
        """
        return int(self.name, 16) >= int(other.name, 16)

    def __le__(self, other):
        """
        Return true if the hexadecimal value of this SHA-1 is less than
        or equal to the other

        :param other: The SHA-1 hash to compare this to
        """
        return int(self.name, 16) <= int(other.name, 16)

    def __eq__(self, other):
        """
        Return True if this SHA-1 hash string matches the other

        :param other: The SHA-1 hash to compare this to
        """
        if isinstance(other, Sha1):
            return self.name == other.name
        return NotImplemented

    def __ne__(self, other):
        """
        Return True if this SHA-1 hash string matches the other

        :param other: The SHA-1 hash to compare this to
        """
        if isinstance(other, Sha1):
            return self.name != other.name
        return NotImplemented

    def __hash__(self):
        return hash(self.name)
