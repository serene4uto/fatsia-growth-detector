from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QComboBox,
    QSizePolicy,
    QMessageBox,
    QPushButton,
)
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from fatsia_growth.services.growth_detector import get_roboflow_model_ids
from fatsia_growth.utils.camera_utils import get_available_cameras


class CameraComboBox(QComboBox):
    
    CURRENT_CAMERAS = {}
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Optionally, you can load cameras initially
        self.load_cameras()

    def showPopup(self):
        self.load_cameras()
        super().showPopup()

    def load_cameras(self):
        try:
            cameras = get_available_cameras()
            if cameras:
                self.clear()
                self.CURRENT_CAMERAS = {}
                for camera_id in cameras:
                    self.CURRENT_CAMERAS[f"Camera {camera_id}"] = camera_id
                    self.addItem(f"Camera {camera_id}")
            else:
                self.clear()
                self.addItem("No Cameras Found")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load cameras:\n{str(e)}")
            self.clear()
            self.addItem("Error Loading Cameras")

class OptionBar(QWidget):
    
    camera_connection_requested = pyqtSignal(int)
    model_toggle_requested = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        self.is_camera_connected = False
        self.is_model_loaded = False
        
        # Set the geometry
        self.setGeometry(0, 0, 1118, 68)  # x=0, y=0, width=1118, height=68
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        self.setSizePolicy(size_policy)
        
        # Create and configure the horizontal layout
        option_layout = QHBoxLayout()
        option_layout.setSpacing(2)
        option_layout.setContentsMargins(4, 0, 0, 0)  # left, top, right, bottom margins
        
        # Camera Option
        camera_label = QLabel("Camera")
        camera_label.setFixedWidth(50)
        option_layout.addWidget(camera_label)
        option_layout.addSpacing(0)
        self.camera_selection_combobox = CameraComboBox()
        self.camera_selection_combobox.setEnabled(True)
        # self.camera_selection_combobox.setMinimumSize(QSize(200, 0))
        self.camera_selection_combobox.setFixedWidth(150)
        option_layout.addWidget(self.camera_selection_combobox)
        option_layout.addSpacing(10)
        self.btn_camera_connection = QPushButton("Connect")
        self.btn_camera_connection.setFixedWidth(100)
        option_layout.addWidget(self.btn_camera_connection)

        option_layout.addSpacing(50)
        
        # Model Option
        model_label = QLabel("Model")
        model_label.setFixedWidth(40)
        option_layout.addWidget(model_label)
        option_layout.addSpacing(0)
        self.model_selection_combobox = QComboBox()
        self.model_selection_combobox.setEnabled(True)
        self.model_selection_combobox.setFixedWidth(200)
        for model_id in get_roboflow_model_ids():
            self.model_selection_combobox.addItem(model_id)
        option_layout.addWidget(self.model_selection_combobox)
        option_layout.addSpacing(10)
        self.btn_model_action = QPushButton("Load")
        self.btn_model_action.setFixedWidth(100)
        option_layout.addWidget(self.btn_model_action)
        
        option_layout.addSpacing(30)
        option_layout.addStretch(1) # Add stretch to push the widgets to the left
        
        # Set the horizontal layout directly to the widget
        self.setLayout(option_layout)
        
        self.btn_camera_connection.clicked.connect(self.on_camera_connection_btn)
        self.btn_model_action.clicked.connect(self.on_model_action_btn)
    
    
    def on_model_action_btn(self):
        if self.is_model_loaded:
            # Request to unload the model
            self.btn_model_action.setText("Unloading...")
            self.btn_model_action.setEnabled(False)
            self.model_toggle_requested.emit("")
        else:
            # Request to load the model
            model_id = self.model_selection_combobox.currentText()
            if model_id:
                self.model_toggle_requested.emit(model_id)
                self.btn_model_action.setText("Loading...")
                self.btn_model_action.setEnabled(False)
            else:
                QMessageBox.critical(
                    self, "Error", "Failed to get model ID."
                )
        
    def on_camera_connection_btn(self):
        if self.is_camera_connected:
            # Request to disconnect the camera
            self.btn_camera_connection.setText("Disconnecting...")
            self.btn_camera_connection.setEnabled(False)
            self.camera_connection_requested.emit(-1) # disconnect request
        else:
            # Request to connect the camera
            camera_id = self.camera_selection_combobox.CURRENT_CAMERAS.get(
                self.camera_selection_combobox.currentText()
            )
            if camera_id is not None:
                self.camera_connection_requested.emit(camera_id)
                self.btn_camera_connection.setText("Connecting...")
                self.btn_camera_connection.setEnabled(False)
                self.camera_selection_combobox.setEnabled(False)        
            else:
                QMessageBox.critical(
                    self, "Error", "Failed to get camera ID."
                )
    
    @pyqtSlot(bool)
    def on_camera_connection_changed(self, connected):
        if not connected:
            # Camera disconnected or failed to connect (#TODO: show error message if failed to connect)
            self.btn_camera_connection.setText("Connect")
            self.is_camera_connected = False
            self.btn_camera_connection.setEnabled(True)
            self.camera_selection_combobox.setEnabled(True)
        else:
            # Camera connected
            self.btn_camera_connection.setText("Disconnect")
            self.is_camera_connected = True
            self.btn_camera_connection.setEnabled(True)
    
    @pyqtSlot(bool)
    def on_model_toggle_status_changed(self, loaded):
        if not loaded:
            # Model unloaded or failed to load (#TODO: show error message if failed to load)
            self.btn_model_action.setText("Load")
            self.is_model_loaded = False
            self.btn_model_action.setEnabled(True)
            self.model_selection_combobox.setEnabled(True)
        else:
            # Model loaded
            self.btn_model_action.setText("Unload")
            self.is_model_loaded = True
            self.btn_model_action.setEnabled(True)
                