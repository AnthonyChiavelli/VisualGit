from PyQt4 import QtGui


class GAnnotatedTag(QtGui.QGraphicsItem):
    """
    A graphics item representing an annotated tag

    Annotated tags mark specific commits (such as those that represent
    a release version of code). Unlike the lightweight tags, which are
    represented by GLightWeightTags, annotated tags cannot be moved,
    and are stored as git objects. Additionally, they can contain
    messages, and can be signed.

    Signed annotated tags are signed using GPG, and provide a way of
    ensuring the authenticity of the tag.

    GAnnotatedTags appear as rectangles containing the relevant data,
    depending on properties of the tag it represents
    """
    pass