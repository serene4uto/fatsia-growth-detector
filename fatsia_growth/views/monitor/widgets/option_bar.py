from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QComboBox,
    QSizePolicy,
)
from PyQt5.QtCore import QSize

from fatsia_growth.utils.camera_utils import get_available_cameras

class OptionBar(QWidget):
    def __init__(self):
        super().__init__()
        
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
        option_layout.addWidget(camera_label)
        
        camera_selection_combobox = QComboBox()
        camera_selection_combobox.setEnabled(True)
        camera_selection_combobox.setMinimumSize(QSize(200, 0))
        camera_selection_combobox.addItem("Camera 1")
        option_layout.addWidget(camera_selection_combobox)
        
        # Model Option
        model_label = QLabel("Model")
        option_layout.addWidget(model_label)
        
        model_selection_combobox = QComboBox()
        model_selection_combobox.setEnabled(True)
        model_selection_combobox.setMinimumSize(QSize(200, 0))
        model_selection_combobox.addItem("Model 1")
        option_layout.addWidget(model_selection_combobox)
      
        # Set the horizontal layout directly to the widget
        self.setLayout(option_layout)
