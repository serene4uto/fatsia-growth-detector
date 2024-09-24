from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

IMAGE_PATH = '/home/serene/fatsia-growth-project/fatsia-growth-detector/app/resources/temp/240623_12_55_02_-063_bmp.rf.ecd02ba6eb52af80f76b867c46f5c6d5.jpg'

# show image
class ResultImageDisplay(QWidget):
    def __init__(self):
        super().__init__()
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter) # center the image
        
        # test
        # Load the image
        self.pixmap = QPixmap(IMAGE_PATH)
        if self.pixmap.isNull():
            self.image_label.setText("Failed to load image.")
        else:
            self.image_label.setPixmap(self.pixmap)
            # self.image_label.setScaledContents(True)  # Allow the pixmap to scale with the label
        
        
    
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)
    
    #TODO: set image
    def set_image(self):
        pass
    
        
        
        
