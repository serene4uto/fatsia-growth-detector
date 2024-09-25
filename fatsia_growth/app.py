import sys
from PyQt5 import QtWidgets, QtCore

from fatsia_growth.app_info import __appname__
from fatsia_growth.views.mainwindow import MainWindow


def main():
    """App entry point"""

    #TODO: parameter here
    
    # Enable scaling for high dpi screens
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_EnableHighDpiScaling, True
    )  # enable highdpi scaling
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_UseHighDpiPixmaps, True
    )  # use highdpi icons
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    
    # Create the Qt app
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(__appname__)
    
    window = MainWindow(
        app=app,
    )
    window.show()

    window.showMaximized()
    window.raise_()
    
    # Run the app
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
    

