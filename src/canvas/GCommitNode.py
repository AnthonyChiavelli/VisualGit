from PyQt4 import QtGui


class GCommitNode(QtGui.QGraphicsItem):
    """
    A graphics item representing a CommitNode

    GCommitNode is a rectangle displaying the sha hash of the commit it
    represents. Parent/child relationships between GCommitNodes are
    shown with a GCommitArrow originating from the child. GCommitNodes
    may be dragged.
    """
    pass