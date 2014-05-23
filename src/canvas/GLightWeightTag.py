from PyQt4 import QtGui


class GLightWeightTag(QtGui.QGraphicsItem):
    """
    A graphics item representing an lightweight tag

    Lightweight tags, unlike annotated tags, are merely references to
    git objects and may be moved around. Additionally, they cannot
    contain additional information beyond a name.

    These are shown as rectangles containing the name of the tag we're
    representing.
    """
    pass