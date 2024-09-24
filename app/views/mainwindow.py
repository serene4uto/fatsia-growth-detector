
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QStatusBar

#TODO: make config file
__appname__ = "fatsia growth detector"
__appdescription__ = "An application to detect the growth of fatsia plants"

class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(
        self,
        # Add any other parameters here
    ):
        super().__init__()

        # Set the window title
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle(__appname__)

        # Set the central widget and the main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Custom widgets go here

        # Set the main layout
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        status_bar = QStatusBar()
        status_bar.showMessage(f"{__appname__} - {__appdescription__}")
        self.setStatusBar(status_bar)


        

        
        

        
