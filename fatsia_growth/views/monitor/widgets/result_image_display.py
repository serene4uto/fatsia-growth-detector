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


# show image
class ResultImageDisplay(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)  # center the image
        self.image_label.setText("Waiting for image.")

        self.pixmap = None
        
        main_layout = QVBoxLayout()
        group_box = QGroupBox()
        image_layout = QVBoxLayout()
        image_layout.addWidget(self.image_label)
        group_box.setLayout(image_layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)
    
    @pyqtSlot(object, object)
    def on_model_result_to_plot(self, frame, results):
        # logger.info("Model result to plot.")
        
        detections = sv.Detections.from_inference(results)
        # create supervision annotators
        bounding_box_annotator = sv.BoundingBoxAnnotator()
        label_annotator = sv.LabelAnnotator()
        
        # annotate the image with our inference results
        annotated_image = bounding_box_annotator.annotate(scene=frame, detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
        
        #TODO: add the FPS to the top left corner
        
        # Convert the numpy array to QImage
        height, width, channel = annotated_image.shape
        bytes_per_line = channel * width
        q_image = QImage(annotated_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        # scale the image
        q_image = q_image.scaled(1280, 720, Qt.KeepAspectRatio)
        
        # Convert QImage to QPixmap
        self.pixmap = QPixmap.fromImage(q_image)

        if self.pixmap.isNull():
            self.image_label.setText("Failed to load image.")
        else:
            self.image_label.setPixmap(self.pixmap)
            # self.image_label.setScaledContents(True)  # Allow the pixmap to scale with the label
            
            
    
    # @pyqtSlot(object)
    # def on_frame_captured(self, frame):
    #     logger.info("Frame captured.")
    #     # Check if the input is a numpy array
    #     if isinstance(frame, np.ndarray):
    #         # Convert the numpy array to QImage
    #         height, width, channel = frame.shape
    #         bytes_per_line = channel * width
    #         q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
    #         # Convert QImage to QPixmap
    #         self.pixmap = QPixmap.fromImage(q_image)
    #     else:
    #         # If frame is not a numpy array, try to directly load it into QPixmap
    #         self.pixmap = QPixmap(frame)
        
    #     if self.pixmap.isNull():
    #         self.image_label.setText("Failed to load image.")
    #     else:
    #         self.image_label.setPixmap(self.pixmap)
    #         # self.image_label.setScaledContents(True)  # Allow the pixmap to scale with the label
