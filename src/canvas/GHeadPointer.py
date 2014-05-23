from PyQt4 import QtGui


class GHeadPointer(QtGui.QGraphicsItem):
    """
    A graphics item representing the current location of HEAD pointer

    The currently checked out commit or branch is referred to by the
    HEAD pointer in git. This graphics item represents the HEAD pointer
    and points to the GCommitNode or GBranchLabel that is checked out.

    The GHeadPointer is a rectangle containing the word HEAD, and
    maintains a connection to its commit or branch with a line.
    """
    pass