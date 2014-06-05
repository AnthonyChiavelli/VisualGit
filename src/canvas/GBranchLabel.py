from PyQt4 import QtGui

# Graphics Properties
from PyQt4.QtCore import QRectF, QPointF
from PyQt4.QtGui import QColor, QFont, QFontMetrics
from model.Branch import Branch

NODE_WIDTH = 60
NODE_HEIGHT = 40
NODE_SELECTED_COLOR = QColor(0, 0, 128)
NODE_UNSELECTED_COLOR = QColor(0, 0, 0)
NODE_TEXT_COLOR = QColor(255, 255, 255)
NODE_TEXT_FONT_SIZE = 9


class GBranchLabel(QtGui.QGraphicsItem):
    """
    A graphics item indicating a Branch

    GBranchLabel is a rectangle containing the name of the branch it
    represents. It is connected to its GCommitNode with a line. A
    GBranchLabel may be dragged around, but will stay in the same
    relative position when a GCommitNode is moved.
    """

    def __init__(self, branch=None):
        """
        Constructor

        :param branch: The git branch to be represented
        """

        super().__init__()
        self._branch = branch

    @property
    def branch(self):
        """ The branch that this represents """
        return self._branch

    def boundingRect(self):
        """
        Define the boundary of this object

        This will determine collision events as well as redrawing
        responsibilities
        """

        return QRectF(0, 0, NODE_WIDTH, NODE_HEIGHT)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        """
        Performs the rendering of the object

        The QPainterObect passed in contains method for drawing various
        shapes, which will then appear on the canvas.

        This node will appear as a rectangle containing the branch name
        """

        # Determine background color based on state of selection
        if self.isSelected():
            QPainter.setBrush(NODE_SELECTED_COLOR)
        else:
            QPainter.setBrush(NODE_UNSELECTED_COLOR)

        # Render the rectangle
        self.paint_rectangle(QPainter)

        # Render the node text
        self.paint_text(QPainter)

    def paint_rectangle(self, QPainter):
        """
        Render the node rectangle

        :param QPainter: interface to the canvas
        """

        QPainter.drawRect(0, 0, NODE_WIDTH, NODE_HEIGHT)

    def paint_text(self, QPainter):
        """
        Render the node text (branch name)

        :param QPainter: interface to the canvas
        """

        # Set up font and text settings
        text_font = QFont()
        text_font.setPointSize(NODE_TEXT_FONT_SIZE)
        QPainter.setFont(text_font)
        QPainter.setPen(NODE_TEXT_COLOR)

        # TODO remove
        _branch = Branch("master", "1423")

        # Measure size of strings so they can be centered properly
        font_metrics = QFontMetrics(text_font)
        label_text_width = font_metrics.width(_branch.name)
        label_text_height = font_metrics.height()

        # Position and render text
        label_margin_left = (NODE_WIDTH - label_text_width) / 2
        label_margin_top = (NODE_HEIGHT - label_text_height) / 2
        label_position = QPointF(label_margin_left, label_margin_top)
        QPainter.drawText(label_position, _branch.name)