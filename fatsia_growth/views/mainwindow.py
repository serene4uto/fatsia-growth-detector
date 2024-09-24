
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QStatusBar

from fatsia_growth.app_info import __appname__, __appdescription__
from fatsia_growth.views.monitor.monitor_widget import MonitorWidget

class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(
        self,
        app=None,
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
        monitor_widget = MonitorWidget()
        main_layout.addWidget(monitor_widget)
        
        # Set the main layout
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        status_bar = QStatusBar()
        status_bar.showMessage(f"{__appname__} - {__appdescription__}")
        self.setStatusBar(status_bar)


        

        
        

        
