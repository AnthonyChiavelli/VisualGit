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
        The line will attach to the point along the border nearest
        the center of the opposite node
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
        self._origin_point = self._calculate_attachment_point(self._origin,
                                                              self._origin_attach_mode,
                                                              self._destination)
        destination_point = self._calculate_attachment_point(self._destination,
                                                             self._destination_attach_mode,
                                                             self._origin)

        # Render a line from the origin to the destination
        self._line = QLineF(self._origin_point, destination_point)
        QPainter.drawLine(self._line)

    def _calculate_attachment_point(self, node, attach_mode, other_node=None):
        """
        Calculate the point on the given node to attach to

        Point will be chosen based on the attach_mode supplied

        :param node: the node for which to calculate the point
        :param attach_mode: the mode of attachment
        :param other_node: the node to which this will be attached,
            needed for some attachment modes
        """

        # Important points needed for calculations
        node_left = node.sceneBoundingRect().left()
        node_right = node.sceneBoundingRect().right()
        node_top = node.sceneBoundingRect().top()
        node_bottom = node.sceneBoundingRect().bottom()
        node_y_mid = node_top + (node.boundingRect().height() / 2)
        node_x_mid = node_left + (node.boundingRect().width() / 2)
        other_node_top = other_node.sceneBoundingRect().top()
        other_node_bottom = other_node.sceneBoundingRect().bottom()
        other_node_left = other_node.sceneBoundingRect().left()
        other_node_right = other_node.sceneBoundingRect().right()
        other_node_center = other_node.sceneBoundingRect().center()

        # Smooth mode: Attachment point will maintain minimum distance
        # to the center of the other node
        if attach_mode == ATTACH_MODE_SMOOTH:

            # If other node is below us
            if other_node_top >= node_bottom:
                # Our line should attach to our bottom...
                y_attach = node_bottom
                # ... in an x position that lines up with the center
                # of the other node
                x_attach = max(min(other_node_center.x(), node_right), node_left)
                return QPointF(x_attach, y_attach)

            # If the other node is to the right
            if other_node_left >= node_right:
                # Our line should attach to our right side...
                x_attach = node_right
                # ... in a y position that lines up with the center of
                # the other node
                y_attach = max(min(other_node_center.y(), node_bottom), node_top)
                return QPointF(x_attach, y_attach)

            # If other node is above us
            if other_node_bottom <= node_top:
                # Our line should attach to our top...
                y_attach = node_top
                # ... in an x position that lines up with the center
                # of the other node
                x_attach = max(min(other_node_center.x(), node_right), node_left)
                return QPointF(x_attach, y_attach)

            # If the other node is to the left
            if other_node_right <= node_left:
                # Our line should attach to our left side...
                x_attach = node_left
                # ... in a y position that lines up with the center of
                # the other node
                y_attach = max(min(other_node_center.y(), node_bottom), node_top)
                return QPointF(x_attach, y_attach)

        # Attachment point will follow center of other node similar to
        # smooth mode, but will snap to the center points of our faces
        if attach_mode == ATTACH_MODE_AUTO_CENTER:

             # If other node is below us
            if other_node_top >= node_bottom:
                # Our line should attach to our bottom center
                return QPointF(node_x_mid, node_bottom)

            # If the other node is to the right
            if other_node_left >= node_right:
                # Our line should attach to our right center
                return QPointF(node_right, node_y_mid)

            # If other node is above us
            if other_node_bottom <= node_top:
                # Our line should attach to our top center
                return QPointF(node_x_mid, node_top)

            # If the other node is to the left
            if other_node_right <= node_left:
                # Our line should attach to our left center
                return QPointF(node_left, node_y_mid)

        # Static attachment modes: attachment will occur at the
        # center of the specified face and remain there regardless of
        # movement
        if attach_mode == ATTACH_MODE_BOTTOM:
            return QPointF(node_x_mid, node_bottom)

        if attach_mode == ATTACH_MODE_TOP:
            return QPointF(node_x_mid, node_top)

        if attach_mode == ATTACH_MODE_LEFT:
            return QPointF(node_left, node_y_mid)

        if attach_mode == ATTACH_MODE_RIGHT:
            return QPointF(node_right, node_y_mid)