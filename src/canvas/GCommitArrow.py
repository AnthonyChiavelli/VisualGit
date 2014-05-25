from canvas.GConnectionLine import GConnectionLine


class GCommitArrow(GConnectionLine):
    """
    A graphics item representing the connection between GCommitNodes

    A GCommitArrow originates from child GCommitNodes and points to
    their parent GCommitNode. GCommitArrows consist of a line and an
    arrow head, and will expand and contract as their source and
    destination nodes are moved around
    """
    pass
