from PyQt4 import QtGui

# Constants defining line attachment strategies
from PyQt4.QtCore import QLineF, QPointF

ATTACH_MODE_TOP = 1
ATTACH_MODE_BOTTOM = 2
ATTACH_MODE_LEFT = 4
ATTACH_MODE_RIGHT = 8
ATTACH_MODE_AUTO_CENTER = 16
ATTACH_MODE_SMOOTH = 32


class GConnectionLine(QtGui.QGraphicsLineItem):
    """
    A straight line that represents a connection between two objects

    This line will maintain correct position as the objects it connects
    (its source and desalination objects) are moved around. It will
    calculate which point to attach to on the two objects based on
    which of the following attachment strategies is chosen for the
    source and destination:

    canvas.GConnectionLine.ATTACH_MODE_TOP
    canvas.GConnectionLine.ATTACH_MODE_BOTTOM
    canvas.GConnectionLine.ATTACH_MODE_LEFT
    canvas.GConnectionLine.ATTACH_MODE_RIGHT
        The line will attach to the middle of the top/bottom/left/right
        face of the node regardless of where the opposite node is

    canvas.GConnectionLine.ATTACH_MODE_AUTO_CENTER
        The line will attach to the middle of the face that the
        opposite node is facing.

    canvas.GConnectionLine.ATTACH_MODE_SMOOTH
        The line will attach to the point nearest the center of the
        opposite node
    """

    def __init__(self, origin, origin_attach_mode, destination, destination_attach_mode):
        """
        Constructor

        :param origin: the node from which this line originates
        :param origin_attach_mode: How the line will attach to its
            origin.
        :param destination: the node into which this line terminates
        :param destination_attach_mode: How the line will attach to its
            destination.
        """

        super().__init__()

        self._origin = origin
        self._origin_attach_mode = origin_attach_mode
        self._destination = destination
        self._destination_attach_mode = destination_attach_mode
        self._line = None
        self._origin_point = None

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        """
        Performs the rendering of the QGraphicsItem

        The QPainterObject passed in contains method for drawing various
        shapes, which will then appear on the canvas.

        This object is a simple line
        """

        # Render the line
        self._render_line(QPainter)

    def _render_line(self, QPainter):
        """
        Render the line

        :param QPainter: Our interface to the canvas
        """

        # Calculate the starting and ending points
        self._origin_point = self._calculate_attachment_point(self._origin, self._origin_attach_mode)
        destination_point = self._calculate_attachment_point(self._destination,
                                                             self._destination_attach_mode)

        # Render a line from the origin to the destination
        self._line = QLineF(self._origin_point, destination_point)
        QPainter.drawLine(self._line)

    def _calculate_attachment_point(self, node, attach_mode):
        """
        Calculate the point on the given node to attach to

        Point will be chosen based on the attach_mode supplied
        """

        node_x_left = node.sceneBoundingRect().left()

        if attach_mode == ATTACH_MODE_BOTTOM:
            node_x_mid = node_x_left + (node.boundingRect().width() / 2)
            node_y_bottom = node.sceneBoundingRect().bottom()
            return QPointF(node_x_mid, node_y_bottom)

        node_y_top = node.sceneBoundingRect().top()

        if attach_mode == ATTACH_MODE_TOP:
            node_x_mid = node_x_left + (node.boundingRect().width() / 2)
            return QPointF(node_x_mid, node_y_top)

        if attach_mode == ATTACH_MODE_LEFT:
            node_y_mid = node_y_top + (node.boundingRect().height() / 2)
            return QPointF(node_x_left, node_y_mid)

        if attach_mode == ATTACH_MODE_RIGHT:
            node_y_mid = node_y_top + (node.boundingRect().height() / 2)
            node_x_right = node.sceneBoundingRect().right()
            return QPointF(node_x_right, node_y_mid)