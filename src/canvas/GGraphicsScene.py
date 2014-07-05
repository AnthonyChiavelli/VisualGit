from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QBrush
from canvas.GBranchLabel import GBranchLabel
from canvas import rendering_algorithms
from PyQt4 import QtGui
from canvas.GCommitArrow import GCommitArrow
from canvas.GCommitNode import GCommitNode
from canvas.GConnectionLine import GConnectionLine

from git.Commit import Commit


# Graphics properties
CANVAS_BACKGROUND_COLOR = QtGui.QColor(232, 232, 232)


class GGraphicsScene(QtGui.QGraphicsScene):
    """
    A QGraphicsScene to display the graphical representation of a repo

    The rendering of canvas graphics occurs in this GGraphicsScene. The
    GGraphicsView (a widget in our layout), will be set to view this
    scene.

    A GGraphicsScene hosts GCommitNodes, GBranchLabels, GCommitArrows,
    and other GGraphicsItem subclasses. It contains the graphs that
    represent a repository.

    Signals:
        commitnode_selected(Commit):
            The CommitNode for the given commit was selected
    """

    # Define Canvas signals
    commitnode_selected = pyqtSignal(Commit)

    def __init__(self):
        """
        Constructor

        Sets up the display settings for this canvas
        """
        super().__init__()

        self.setBackgroundBrush(QBrush(CANVAS_BACKGROUND_COLOR))

        # A mapping of sha to GCommitNode to avoid redrawing the same
        # node twice (as it may be a child of multiple parents)
        self._sha_to_node = {}


    def render_scene(self, commit, branches):
        """
        Renders the various elements of the canvas

        First, the commits are parsed recursively and rendered onto
        the canvas as GCommitNodes in a graph arrangement. Arrows
        are drawn to show parent-child relationships.

        Then, branch and tag labels are drawn next to their commits

        :param commit: The root of the commit tree to render
        :param branches: The branches of the commit tree to render
        """

        # Convert our Commit tree to a tree of GCommitNode objects
        root_g_commit_node = self._node_tree_from_commit(commit)

        # Measure layout of tree with chosen algorithm
        rendering_algorithms.minimum_width(root_g_commit_node)

        # Render commits onto canvas
        self._render_commit_tree(root_g_commit_node)

        # Render branches onto the canvas
        self._render_branch_labels(branches)

    def _render_commit_tree(self, g_commit_node):
        """
        Render a tree/graph of commits onto the canvas

        GCommitNodes are the graphical objects that represent and
        encapsulate commit nodes. Previously our tree of Commit objects
        has been traversed and each node converted to a GCommitNode and
        assigned coordinates based on the particular tree drawing
        algorithm chosen. This method simple renders each node at its
        given x and y coordinates in a preorder traversal.

        While drawing nodes, we also draw arrows to indicate a parent
        child relationship between nodes.
        """

        # Add this node to the scene
        self.addItem(g_commit_node)

        # For each child node
        for child in g_commit_node.children:
            # Render an arrow from child to parent
            commit_arrow = GCommitArrow(g_commit_node,
                                        GConnectionLine.ATTACH_MODE_SMOOTH,
                                        child,
                                        GConnectionLine.ATTACH_MODE_AUTO_CENTER)
            self.addItem(commit_arrow)

            # And recursively render child
            self._render_commit_tree(child)

    def _node_tree_from_commit(self, commit, parent=None):
        """
        Converts a Commit tree into a GCommitNode tree

        Commit objects represent commits made in a repository. They are
        represented by, and aggregated by, GCommitNode objects, which
        are graphics objects that can be drawn on the canvas.

        This method traverses a tree rooted at the provided Commit and
        constructs a GCommitNode tree of the same structure, preserving
        parent-child relationships.
        """

        num_of_children = len(commit.children)

        # Make sure we haven't already processed this commit (via
        # another parent)
        # Grab the existing one if present
        if commit.sha in self._sha_to_node:
            g_commit_node = self._sha_to_node[commit.sha]
        # Otherwise we need a new one
        else:
            g_commit_node = GCommitNode(commit)

        # If this is a recursive call, attach calling parent
        if parent:
            g_commit_node.parents.append(parent)

        # If our commit has children, recursively call ourselves
        # on each child and add the gcommitnode returned to our
        # children set
        for commit_child in commit.children:
            new_g_commit_node = self._node_tree_from_commit(commit_child, g_commit_node)
            g_commit_node.children.append(new_g_commit_node)

        # Add this to our global mapping of shas to gcommitnodes
        self._sha_to_node[commit.sha] = g_commit_node

        # Return newly converted gcommitnode
        return g_commit_node

    def _render_branch_labels(self, branches):
        """
        Render branch labels next to, and connected to, the commits
        to which they point.

        :param branches: The branches whose labels are to be rendered
        """

        # For each branch
        for branch in branches:
            # Create a representing branch label
            new_branch_label = GBranchLabel(branch)

            # Attach it to its commit via arrow
            corresponding_commit = self._sha_to_node[branch.commit_sha]
            new_branch_label.setPos(corresponding_commit.pos().x() + 150,
                                    corresponding_commit.pos().y())
            new_connection_line = GConnectionLine(corresponding_commit,
                                                  GConnectionLine.ATTACH_MODE_SMOOTH,
                                                  new_branch_label,
                                                  GConnectionLine.ATTACH_MODE_LEFT)

            # Associate it with its commit corresponding_commit
            corresponding_commit.add_branch_label(new_branch_label)

            # Render connection line and label
            self.addItem(new_branch_label)
            self.addItem(new_connection_line)