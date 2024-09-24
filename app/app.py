import sys
from PyQt5 import QtWidgets

from views import MainWindow

def main():
    """App entry point"""

    #TODO: parameter here

    # Create the Qt app
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    window.showMaximized()
    window.raise_()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

