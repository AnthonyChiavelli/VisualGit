import sys
from PyQt4 import QtGui, uic
from canvas.GGraphicsScene import GGraphicsScene


class MainApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Load and display UI file
        self.ui = uic.loadUi('/home/anthony/dev/projects/VisualGit/ui/mainwindow.ui')

        # Add a graphics scene for the graphics view in our UI
        scene = GGraphicsScene()
        self.ui.graphicsView.setScene(scene)

        # Test shape
        ellipse = QtGui.QGraphicsEllipseItem()
        ellipse.setRect(0.0, 0.0, 20.0, 20.0)
        ellipse.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        scene.addItem(ellipse)

        self.ui.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = MainApp()
    sys.exit(app.exec_())
