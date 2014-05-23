from PyQt4 import QtGui


class GConnectionLine(QtGui.QGraphicsItem):
    """
    A straight line that represents a connection between two objects

    This line will maintain correct position as the objects it connects
    are moved around. It will calculate which point to attach to on the
    two objects based on which point calculation strategies are chosen.
    """
    pass