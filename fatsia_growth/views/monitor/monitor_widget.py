from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout, 
    QHBoxLayout, 
)

from PyQt5.QtCore import pyqtSlot

from fatsia_growth.utils.logger import logger
from fatsia_growth.views.monitor.widgets import (
    ResultImageDisplay,
    OptionBar,
    ResultListDisplay,
)

from fatsia_growth.services.camera_service import CameraService
from fatsia_growth.services.growth_detector import GrowthDetector
from fatsia_growth.services.results_uploader import ResultsUploader

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
        
        self.option_bar = OptionBar()
        self.option_bar.setFixedHeight(100)
        self.option_bar.camera_connection_requested.connect(
            self.on_camera_connection_requested
        )  
        self.option_bar.model_toggle_requested.connect(
            self.on_model_toggle_requested
        )  
        self.option_bar.upload_server_requested.connect(
            self.on_upload_server_requested
        )       
        
        self.result_image_display = ResultImageDisplay()        
        
        central_layout.addWidget(self.option_bar)
        central_layout.addWidget(self.result_image_display)
        
        
        #TODO: create a left layout
        left_layout = QVBoxLayout()
        layout.addLayout(left_layout)
        
        #TODO: create a right layout
        right_layout = QVBoxLayout()
        
        self.result_list_display = ResultListDisplay()
        right_layout.addWidget(self.result_list_display)
        
        
        layout.addLayout(right_layout)
        
        # set the layout
        self.setLayout(layout)
        
        # Services
        self.camera_service = CameraService()
        self.growth_detector = GrowthDetector()
        self.results_uploader = ResultsUploader()
        
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
        self.growth_detector.model_result_image_plot_signal.connect(
            self.result_image_display.on_model_result_to_plot
        )
        self.growth_detector.model_result_upload_signal.connect(
            self.on_model_result_upload_signal
        )
        self.growth_detector.model_result_display_signal.connect(
            self.result_list_display.on_model_result_display_signal
        )
        
    
    @pyqtSlot(object, object)
    def on_model_result_upload_signal(self, frame, result):
        if not self.results_uploader.thread.isRunning():
            return
        
        if self.results_uploader.results_queue.full():
            # make space by removing the oldest item
            self.results_uploader.results_queue.get()
        self.results_uploader.results_queue.put((frame, result))
        
    @pyqtSlot(object)
    def on_camera_frame_captured(self, frame):
        if not self.growth_detector.thread.isRunning():
            return
        
        if self.growth_detector.frame_queue.full():
            # make space by removing the oldest item
            self.growth_detector.frame_queue.get()

        self.growth_detector.frame_queue.put(frame)
    
    @pyqtSlot(str)
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
    
    @pyqtSlot(int)
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
    
    @pyqtSlot(bool)
    def on_upload_server_requested(self, upload):
        if upload:
            
            self.growth_detector.model_result_upload = True # Enable result upload
            
            # Start the results uploader
            if self.results_uploader.thread.isRunning():
                self.results_uploader.stop()
            
            self.results_uploader.start()
        else:
            
            self.growth_detector.model_result_upload = False # Disable result upload
            
            # Stop the results uploader
            if self.results_uploader.thread.isRunning():
                self.results_uploader.stop()
        
        
        
        

        
        
        
        
        