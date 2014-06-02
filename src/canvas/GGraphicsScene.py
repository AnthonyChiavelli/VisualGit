from PyQt4 import QtGui

# Graphics properties
from PyQt4.QtGui import QBrush

CANVAS_BACKGROUND_COLOR = QtGui.QColor(232, 232, 232)


class GGraphicsScene(QtGui.QGraphicsScene):
    """
    A QGraphicsScene to display the graphics representation of a repo

    The rendering of canvas graphics occurs in this GGraphicsScene. The
    GGraphicsView (a widget in our layout), will be set to view this
    scene.

    A GGraphicsScene hosts GCommitNodes, GBranchLabels, GCommitArrows,
    and other GGraphicsItem subclasses. It contains the graphs that
    represent a repository.
    """

    def __init__(self):
        """
        Constructor

        Sets basic display options for this canvas
        """
        super().__init__()

        self.setBackgroundBrush(QBrush(CANVAS_BACKGROUND_COLOR))

        # A mapping of sha to GCommitNode to avoid redrawing the same
        # node twice (as it may be a child of multiple parents)
        self.sha_to_node = {}


    def render_scene(self, commit):
        """
        Renders the various elements of the canvas

        First, the commits are parsed recursively and rendered onto
        the canvas as GCommitNodes in a tree arrangement. Arrows
        are drawn to show parent-child relationships.

        Then, branch and tag labels are drawn next to their commitss
        """

        # Convert our Commit tree to a tree of GCommitNode objects


        # Generate graphical tree from root commit using chosen
        # algorithm
        # TODO
        self._render_commits(None)

        # Render labels
        # TODO

    def _render_commits(self, g_commit_node):
        """
        Render a graph of commits onto the canvas

        GCommitNodes are the graphical objects that represent and
        encapsulate commit nodes. Previously our tree of Commit objects
        has been traversed and each node converted to a GCommitNode and
        assigned coordinates based on the particular tree drawing
        algorithm chosen. This method simple renders each node at its
        given x and y coordinates in a preorder traversal.
        """

        # Add this node to the scene
        self.addItem(g_commit_node)

        # Recursively call on its children to be added to scene
        map(self._render_commits, g_commit_node.children)

    def node_tree_from_commit(self, commit, parent = None):
        """
        Converts a Commit tree into a GCommitNode tree

        Commit objects represent commits made in a repository. They are
        represented by, and aggregated by, GCommitNode objects, which
        are graphics objects that can be drawn on the canvas.

        This method traverses a tree rooted at the provided Commit and
        constructs a GCommitNode tree of the same structure, preserving
        parent-child relationships.
        """

        # Make sure we haven't already processed this commit (via
        # another parent)
        if commit.sha in self.sha_to_node:
            g_commit_node = self.sha_to_node[commit.sha]
        # Otherwise we need a new one
        else:
            g_commit_node = GCommitNode(commit)

        # If this is a recursive call, attach calling parent
        if parent:
            g_commit_node.parents.append(parent)

        # If our commit has children, recursively call ourselves
        # on each child and add the gcommitnode returned to our
        # children set
        if commit.children:
            for commit_child in commit.children:
                new_g_commit_node = self.node_tree_from_commit(commit_child, g_commit_node)
                g_commit_node.children.append(new_g_commit_node)
            # TODO handle arrows

        # Add this to our global mapping of shas to gcommitnodes
        self.sha_to_node[commit.sha] = g_commit_node

        # Return newly converted gcommitnode
        return g_commit_node