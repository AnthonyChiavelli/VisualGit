from PyQt4 import QtGui

# Graphics properties
from PyQt4.QtGui import QBrush

CANVAS_BACKGROUND_COLOR = QtGui.QColor(232, 232, 232)


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

    def __init__(self):
        """
        Constructor

        Sets basic display options for this canvas
        """
        super().__init__()

        self.setBackgroundBrush(QBrush(CANVAS_BACKGROUND_COLOR))
