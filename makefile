# Generate UI Python modules
ui/mainwindow.py : ui/mainwindow.ui
		pyuic4 -x ui/mainwindow.ui -o ui/mainwindow.py