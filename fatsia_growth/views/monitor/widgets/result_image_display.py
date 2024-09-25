from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage
import numpy as np

from fatsia_growth.utils.logger import logger

IMAGE_PATH = '/home/serene/fatsia-growth-project/fatsia-growth-detector/fatsia_growth/resources/temp/240623_12_55_02_-063_bmp.rf.ecd02ba6eb52af80f76b867c46f5c6d5.jpg'

# show image
class ResultImageDisplay(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)  # center the image
        
        # test
        # Load the image
        self.pixmap = QPixmap(IMAGE_PATH)
        if self.pixmap.isNull():
            self.image_label.setText("Failed to load image.")
        else:
            self.image_label.setPixmap(self.pixmap)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)
    
    @pyqtSlot(object)
    def on_frame_captured(self, frame):
        logger.info("Frame captured.")
        # Check if the input is a numpy array
        if isinstance(frame, np.ndarray):
            # Convert the numpy array to QImage
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # Convert QImage to QPixmap
            self.pixmap = QPixmap.fromImage(q_image)
        else:
            # If frame is not a numpy array, try to directly load it into QPixmap
            self.pixmap = QPixmap(frame)
        
        if self.pixmap.isNull():
            self.image_label.setText("Failed to load image.")
        else:
            self.image_label.setPixmap(self.pixmap)
            # self.image_label.setScaledContents(True)  # Allow the pixmap to scale with the label
