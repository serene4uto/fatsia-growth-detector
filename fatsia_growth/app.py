import sys
import logging
from PyQt5 import QtWidgets, QtCore


from fatsia_growth.app_info import __appname__
from fatsia_growth.views.mainwindow import MainWindow

from fatsia_growth.utils.logger import logger, ColoredFormatter, ColoredLogger


def main():
    """App entry point"""

    #TODO: parameter here
    
    # Set up the logger
    logger.setLevel(logging.DEBUG)
    if not logger.hasHandlers():
        # This block ensures that the logger has a handler after class change
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = ColoredFormatter(ColoredLogger.FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    
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
    
    

