from PyQt4 import QtGui


class GBranchLabel(QtGui.QGraphicsScene):
    """
    A graphics item indicating a Branch

    GBranchLabel is a rectangle containing the name of the branch it
    represents. It is connected to its GCommitNode with a line. A
    GBranchLabel may be dragged around, but will stay in the same
    relative position when a GCommitNode is moved.
    """
    pass
