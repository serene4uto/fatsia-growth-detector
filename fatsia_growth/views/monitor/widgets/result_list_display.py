from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QTableView,
    QGroupBox,
    QHeaderView,
)
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import (
    QStandardItemModel, 
    QStandardItem,
)
from fatsia_growth.utils.logger import logger


class ResultListDisplay(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize the main layout
        main_layout = QVBoxLayout()
        
        # Create a group box to contain the table view
        group_box = QGroupBox("Results")
        result_layout = QVBoxLayout()
        
        # Initialize the table view and its model
        self.result_view = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        self.model.setHorizontalHeaderLabels([
            # "Class ID", 
            "Class", 
            "Confidence", 
            # "Class Confidence", 
            "Bounding Box"
        ])
        self.result_view.setModel(self.model)
        
        # Configure header resize modes
        header = self.result_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        # Set the fixed widths for specific columns
        self.result_view.setColumnWidth(0, 150)
        self.result_view.setColumnWidth(1, 150) 
        self.result_view.setColumnWidth(2, 150)
        
        # Apply stylesheet for grid lines and header styling
        self.result_view.setStyleSheet("""
            QTableView {
                gridline-color: #d3d3d3;
                border: 1px solid #c0c0c0;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: #333333;
                padding: 4px;
                border: 1px solid #c0c0c0;
            }
            QTableView::item {
                border-bottom: 1px solid #d3d3d3;
                border-right: 1px solid #d3d3d3;
            }
            /* Optional: Remove the last vertical line for a cleaner look */
            QTableView::item:last-column {
                border-right: none;
            }
        """)
        
        # Add the table view to the layout
        result_layout.addWidget(self.result_view)
        
        # Set the layout for the group box and add it to the main layout
        group_box.setLayout(result_layout)
        main_layout.addWidget(group_box)
        
        # Set the main layout for the widget
        self.setLayout(main_layout)
    
    @pyqtSlot(object)
    def on_model_result_display_signal(self, results):

        logger.info(f"Updating table with results: {results}")
        
        # Clear existing data while preserving headers
        self.model.setRowCount(0)
        
        # Iterate over the predictions and populate the table
        for prediction in results.predictions:
            # Create items for each column
            
            item_data = [
                #QStandardItem(str(prediction.class_id)),
                QStandardItem(prediction.class_name),
                QStandardItem(f"{prediction.confidence:.2f}"),
                # QStandardItem(f"{prediction.class_confidence}"),
                QStandardItem(f"(x: {prediction.x}, y: {prediction.y}, w: {prediction.width}, h: {prediction.height})")
            ]
            
            # Optionally, align text to center for better readability
            for item in item_data:
                item.setTextAlignment(Qt.AlignCenter)
            
            # Append the row to the model
            self.model.appendRow(item_data)
        
        # Optionally, resize rows to fit contents
        self.result_view.resizeRowsToContents()
        
