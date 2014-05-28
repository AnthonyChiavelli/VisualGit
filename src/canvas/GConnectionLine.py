from PyQt4 import QtGui

# Constants defining line attachment strategies
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
        self._origin = origin
        self._origin_attach_mode = origin_attach_mode
        self._destination = destination
        self._destination_attach_node = destination_attach_mode

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        """
        Performs the rendering of the QGraphicsItem

        The QPainterObject passed in contains method for drawing various
        shapes, which will then appear on the canvas.

        This object is a simple line
        """

        # Render the line
        self.render_line(QPainter)

    def render_line(QPainter):
        """
        Render the line

        Performs the rendering of the item.


        """
        pass