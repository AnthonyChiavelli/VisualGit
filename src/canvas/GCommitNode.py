from PyQt4 import QtGui

from PyQt4.QtCore import QRectF, QPointF
from PyQt4.QtGui import QColor, QFont, QFontMetrics

# Graphics properties
NODE_WIDTH = 75
NODE_HEIGHT = 50
NODE_CORNER_RADIUS = 2.5
NODE_SELECTED_COLOR = QColor(229, 150, 47)
NODE_UNSELECTED_COLOR = QColor(99, 102, 133)
NODE_TEXT_COLOR = QColor(255, 255, 255)
NODE_TEXT_FONT_SIZE = 9
NODE_LABEL_TEXT = 'commit'


class GCommitNode(QtGui.QGraphicsItem):
    """
    A graphics item representing a CommitNode

    GCommitNode is a rectangle displaying the sha hash of the commit it
    represents. Parent/child relationships between GCommitNodes are
    shown with a GCommitArrow originating from the child. GCommitNodes
    may be dragged.

    Inside a GCommitNode, there are two strings, a string labeling this
    as a commit, and a sha string, showing the sha of the commit.
    """

    def __init__(self, commit_node=None):
        """
        Constructor

        Sets up the properties of the node

        :param commit_node: the CommitNode this GCommitNode represents
        """

        super().__init__()
        self._commit_node = commit_node
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

    @property
    def commit_node(self):
        """ The commit node that this represents """
        return self._commit_node

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

        # Render the rectangle
        self.paint_rectange(QPainter)

        # Render the node text
        self.paint_text(QPainter)

    def paint_rectange(self, QPainter):
        """
        Renders the node rectangle

        :param QPainter: interface to the canvas
        """

        QPainter.drawRoundedRect(0, 0, NODE_WIDTH, NODE_HEIGHT, NODE_CORNER_RADIUS, NODE_CORNER_RADIUS)

    def paint_text(self, QPainter):
        """
        Render the node text (commit sha and label)

        :param QPainter: interface to the canvas
        """

        #TODO remove
        temp_commit_sha = "4"

        # Set up font and text settings
        text_font = QFont()
        text_font.setPointSize(NODE_TEXT_FONT_SIZE)
        QPainter.setFont(text_font)
        QPainter.setPen(NODE_TEXT_COLOR)

        # Measure size of strings so they can be centered properly
        font_metrics = QFontMetrics(text_font)
        label_text_width = font_metrics.width(NODE_LABEL_TEXT)
        sha_text_width = font_metrics.width(temp_commit_sha)

        # Position and render text
        label_margin = (NODE_WIDTH - label_text_width) / 2
        label_position = QPointF(label_margin, 15)
        QPainter.drawText(label_position, NODE_LABEL_TEXT)
        sha_margin = (NODE_WIDTH - sha_text_width) / 2
        sha_position = QPointF(sha_margin, 25)
        QPainter.drawText(sha_position, temp_commit_sha)