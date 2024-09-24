from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from fatsia_growth.views.monitor.widgets import (
    ResultImageDisplay,
    OptionBar
)

class MonitorWidget(QWidget):
    def __init__(
        self
    ):
        super().__init__()
        
        # create a layout
        layout = QHBoxLayout()
        
        # create a central layout
        central_layout = QVBoxLayout()
        
        
        layout.addLayout(central_layout)
        # self.label_options = QLabel("Options")
        # central_layout.addWidget(self.label_options)
        self.option_bar = OptionBar()
        self.result_image_display = ResultImageDisplay()
        
        
        central_layout.addWidget(self.option_bar)
        central_layout.addWidget(self.result_image_display)
        
        
        
        
        
        #TODO: create a left layout
        left_layout = QVBoxLayout()
        layout.addLayout(left_layout)
        
        #TODO: create a right layout
        right_layout = QVBoxLayout()
        layout.addLayout(right_layout)
        
        
        
        
        
        # set the layout
        self.setLayout(layout)
    
    def get_label_options(self):
        
        return self.label_options
        

        
        
        

        
        
        
        
        