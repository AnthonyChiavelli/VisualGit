"""
A collection of algorithms for drawing a tree/graph

These generic algorithms traverse a tree and assign an x and y
coordinates to each node in the tree. Drawing a tree is an np-complete
problem, and drawing an attractive tree is a human problem; both are
unsolvable. Various tree drawing algorithms exist, each with guiding
principles, and problems they attempt to solve.

Some common principles of tree drawing include:
1. Connecting lines should not cross
2. Nodes within the same depth should be drawn in line with each other
3. Parents should be centered above their children
4. The tree should not be wider than necessary

Git repositories are not actually trees, but acyclic directed graphs.
As such, we may often have to forgo some of the principles listed
above, and we must apply modifications to the algorithms used. However,
because git repos are usually mostly tree-like, and many people prefer
to visualize them in a hierarchy, we still opt to use tree-drawing
strategies and make the necessary corrections.
"""


def minimum_width(root_commit):
    """
    Draw a minimally wide tree

    This algorithm produces a tree of minimum width, with each
    generation on a different row. The tree begins at the top and grows
    downward. Though for general purposes the trees drawn by this are
    considered somewhat ugly, their narrow, linear shape is decently
    well-suited for git repos.

    In particular, children of a node are drawn the next level down,
    at the left-most available x position. The results in a compact,
    linear tree, but lineage can be difficult to follow.

    :param root_commit: the root commit of the tree to be rendered
    """
    _minimum_width(root_commit)


def _minimum_width(g_commit_node, next_x_slots=[0], depth=0):
    """
    Helper function for minimum_width()

    This helper function performs the actual rendering.

    :param g_commit_node: The current GCommitNode being processed
    :param next_x_slots: Keeps track of the next available x position
        for each row
    :param depth: the depth of the current commit being processed
    """

    # Position based on depth (y) and left-most available column (x)
    x_spacing, y_spacing = 100, 100  # TODO accept as setting parameter
    x_pos = next_x_slots[depth] * x_spacing
    y_pos = depth * y_spacing
    g_commit_node.setPos(x_pos, y_pos)

    # Column at this depth was used, move on to next one
    next_x_slots[depth] += 1

    # Draw children at next lower level
    for child in g_commit_node.children:
        next_x_slots.append(0)
        _minimum_width(child, next_x_slots, depth + 1)