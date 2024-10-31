from PyQt5.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout,
    QGroupBox,
)

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
import supervision as sv
from fatsia_growth.utils.logger import logger
import cv2
import time
from collections import deque


# show image
class ResultImageDisplay(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)  # center the image
        self.image_label.setText("Waiting for image.")

        self.pixmap = None

        # Initialize FPS tracking variables with a deque for averaging
        self.last_times = deque(maxlen=30)  # Store timestamps of the last 30 frames
        self.fps = 0.0
        
        main_layout = QVBoxLayout()
        group_box = QGroupBox()
        image_layout = QVBoxLayout()
        image_layout.addWidget(self.image_label)
        group_box.setLayout(image_layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)
    
    @pyqtSlot(object, object)
    def on_model_result_to_plot(self, frame, results):
        # Append current time to the deque
        current_time = time.time()
        self.last_times.append(current_time)
        
        # Calculate FPS as the number of frames divided by the time difference
        if len(self.last_times) >= 2:
            time_diff = self.last_times[-1] - self.last_times[0]
            if time_diff > 0:
                self.fps = (len(self.last_times) - 1) / time_diff

        detections = sv.Detections.from_inference(results)
        # create supervision annotators
        bounding_box_annotator = sv.BoundingBoxAnnotator()
        label_annotator = sv.LabelAnnotator()
        
        # annotate the image with our inference results
        annotated_image = bounding_box_annotator.annotate(scene=frame, detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
        
        # Add FPS to the top-left corner
        fps_text = f"FPS: {self.fps:.2f}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (0, 255, 0)  # Green color in BGR
        thickness = 2
        position = (10, 30)  # Top-left corner
        
        cv2.putText(annotated_image, fps_text, position, font, font_scale, color, thickness, cv2.LINE_AA)
        
        # Convert the numpy array to QImage
        height, width, channel = annotated_image.shape
        bytes_per_line = channel * width
        q_image = QImage(annotated_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        q_image = q_image.rgbSwapped()  # BGR to RGB
        
        # scale the image
        q_image = q_image.scaled(1280, 720, Qt.KeepAspectRatio)
        
        # Convert QImage to QPixmap
        self.pixmap = QPixmap.fromImage(q_image)

        if self.pixmap.isNull():
            self.image_label.setText("Failed to load image.")
        else:
            self.image_label.setPixmap(self.pixmap)
            # self.image_label.setScaledContents(True)  # Allow the pixmap to scale with the label
