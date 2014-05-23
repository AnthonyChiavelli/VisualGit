from PyQt4 import QtGui


class GGraphicsScene(QtGui.QGraphicsScene):
    """
    A QGraphicsScene to display the graphics representation of a repo

    The rendering of canvas graphics occurs in this GGraphicsScene. The
    GGraphicsView (a widget in our layout), will be set to view this
    scene.

    A GGraphicsScene hosts GCommitNodes, GBranchLabels, GCommitArrows,
    and other GGraphicsItem subclasses. It contains the graphs that
    represent a repository.
    """
    pass
