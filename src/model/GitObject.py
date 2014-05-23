class GitObject():
    """
    A git data object, identified by it's SHA-1 hash value.

    There are four main types of git objects: blobs, trees, commits,
    and tags. Git objects are identified by their SHA-1 hash value.
    Although the hash is 40 characters long, 6 or 7 characters will
    almost always provide a unique identifier within even large
    repositories.

    All git objects are stored in the local repository, in the
    .git/objects/ directory, compressed using the zlib format. They
    organized into directories corresponding to the first two
    characters of the object's SHA-1 hash, and file names corresponding
    to the last 38 characters of the SHA-1.
    """

    def __init__(self, sha):
        """
        Constructor.
        """
        self._sha = sha

    def get_subdirectory_name(self):
        """
        Returns the name of the subdirectory this git object is stored in (the first two characters
        of the SHA-1)
        """
        return self.sha.get_string_of_length(2)

    def get_file_name(self):
        """
        Returns the name of the file containing this git object (the last 38 characters of the
        SHA-1)
        """
        return str(self.sha)[2:40]

    @property
    def sha(self):
        """
        The SHA-1 hash string used to identify this git object.
        """
        return self._sha