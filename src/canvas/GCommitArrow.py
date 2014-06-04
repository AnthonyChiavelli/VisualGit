from math import acos, pi, sin, cos
from PyQt4.QtCore import QPointF, Qt
from PyQt4.QtGui import QBrush
from canvas.GConnectionLine import GConnectionLine

# Graphics properties
ARROW_HEAD_WIDTH = 7
ARROW_HEAD_LENGTH = 10
ARROW_HEAD_BRUSH = QBrush(Qt.black)


class GCommitArrow(GConnectionLine):
    """
    A graphics item representing the connection between GCommitNodes

    A GCommitArrow originates from child GCommitNodes and points to
    their parent GCommitNode. GCommitArrows consist of a line and an
    arrow head, and will expand and contract as their source and
    destination nodes are moved around
    """

    def __init__(self, origin, origin_attach_mode, destination, destination_attach_mode):
        """
        Constructor

        :param origin: the node from which this line originates
        :param destination: the node at which this line terminates
        """

        super().__init__(origin, origin_attach_mode, destination, destination_attach_mode)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        """
        Performs the rendering of the QGraphicsItem

        The QPainterObject passed in contains method for drawing various
        shapes, which will then appear on the canvas.

        This object is a simple line with an arrow head indicating the
        destination of the line.
        """

        self._render_line(QPainter)
        self._render_head(QPainter)

    def _render_head(self, QPainter):
        # Calculate the angle of our line
        angle_of_line = acos(self._line.dx() / self._line.length())

        # Make angle relative to correct line of reference
        if self._line.dy() >= 0:
            angle_of_line = (pi * 2) - angle_of_line

        # Calculate the two points which, along with the end of the
        # line, form the triangular arrow head

        head_point1 = self._origin_point + QPointF(
            sin(angle_of_line + pi / 3) * ARROW_HEAD_WIDTH,
            cos(angle_of_line + pi / 3) * ARROW_HEAD_LENGTH)
        head_point2 = self._origin_point + QPointF(
            sin(angle_of_line + pi - pi / 3) * ARROW_HEAD_WIDTH,
            cos(angle_of_line + pi - pi / 3) * ARROW_HEAD_LENGTH)

        # Use the brush to fill in arrow head
        QPainter.setBrush(ARROW_HEAD_BRUSH)

        # Use the three points to draw the polygon
        QPainter.drawPolygon(self._origin_point, head_point1, head_point2)