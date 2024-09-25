from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from fatsia_growth.utils.logger import logger
from fatsia_growth.views.monitor.widgets import (
    ResultImageDisplay,
    OptionBar
)

from fatsia_growth.services.camera_service import CameraService
from fatsia_growth.services.growth_detector import GrowthDetector

class MonitorWidget(QWidget):
    def __init__(
        self
    ):
        super().__init__()
        
        #define actions
        
        # create a layout
        layout = QHBoxLayout()
        
        # create a central layout
        central_layout = QVBoxLayout()
        
        
        layout.addLayout(central_layout)
        # self.label_options = QLabel("Options")
        # central_layout.addWidget(self.label_options)
        self.option_bar = OptionBar()
        self.option_bar.camera_connection_requested.connect(
            self.on_camera_connection_requested
        )  
        self.option_bar.model_toggle_requested.connect(
            self.on_model_toggle_requested
        )          
        
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
        
        
        self.camera_service = CameraService()
        self.growth_detector = GrowthDetector()
        
        
        self.camera_service.camera_connection_changed.connect(
            self.option_bar.on_camera_connection_changed
        )
        self.camera_service.frame_captured.connect(
            # self.result_image_display.on_frame_captured
            self.on_camera_frame_captured
        )
        
        self.growth_detector.model_toggle_status_changed.connect(
            self.option_bar.on_model_toggle_status_changed
        )
        
        
    def on_camera_frame_captured(self, frame):
        # logger.info("Frame captured.")
        self.growth_detector.frame_queue.put(frame)
    
    def on_model_toggle_requested(self, model_id):
        if model_id == "":
            # Stop the model service
            if self.growth_detector.thread.isRunning():
                self.growth_detector.stop()
        else:
            # Start the model service
            
            if self.growth_detector.thread.isRunning():
                self.growth_detector.stop()
            
            self.growth_detector.start(model_id)
        
    def on_camera_connection_requested(self, camera_id):
        if camera_id < 0:
            # Stop the camera service
            if self.camera_service.thread.isRunning():
                self.camera_service.stop()
            return
        else:
            # Start the camera service
            if self.camera_service.thread.isRunning():
                self.camera_service.stop()

            self.camera_service.start(camera_id)
        
        
        
        

        
        
        
        
        