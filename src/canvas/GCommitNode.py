from PyQt4 import QtGui

# Graphics properties
from PyQt4.QtCore import QRectF
from PyQt4.QtGui import QColor

NODE_WIDTH = 75
NODE_HEIGHT = 50
NODE_CORNER_RADIUS = 2.5
NODE_SELECTED_COLOR = QColor(229, 150, 47)
NODE_UNSELECTED_COLOR = QColor(99, 102, 133)


class GCommitNode(QtGui.QGraphicsItem):
    """
    A graphics item representing a CommitNode

    GCommitNode is a rectangle displaying the sha hash of the commit it
    represents. Parent/child relationships between GCommitNodes are
    shown with a GCommitArrow originating from the child. GCommitNodes
    may be dragged.
    """
    def __init__(self):
        """
        Constructor

        Sets up the properties of the node
        """
        super().__init__()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

    def boundingRect(self):
        """
        Define the boundary of this object

        We assume a rectangle with the same size as our rounded
        rectangle.
        """
        return QRectF(0, 0, NODE_WIDTH, NODE_HEIGHT)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        """
        Performs the rendering of the object

        The QPainterObect passed in contains method for drawing various
        shapes, which will then appear on the canvas.
        """

        # Determine background color based on state of selection
        if self.isSelected():
            QPainter.setBrush(NODE_SELECTED_COLOR)
        else:
            QPainter.setBrush(NODE_UNSELECTED_COLOR)

        QPainter.drawRoundedRect(0, 0, NODE_WIDTH, NODE_HEIGHT, NODE_CORNER_RADIUS, NODE_CORNER_RADIUS)