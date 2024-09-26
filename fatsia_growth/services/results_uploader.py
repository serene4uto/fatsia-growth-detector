from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
import queue
from datetime import datetime
import requests
import base64
import cv2
from fatsia_growth.utils.logger import logger
from fatsia_growth.schemas.fatsia import GrowthStageData, Detection, BoundingBox, ImageData

DEVICE_ID = "fatsia_001"    
SERVER_URL =  "http://127.0.0.1:8000"
RESULT_UPLOAD_ENDPOINT = "fatsia/growth"

def encode_image_frame_to_base64(frame):
    """Encodes a frame to a base64 string."""
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        logger.error("Could not encode frame to JPEG.")
        return None
    return base64.b64encode(buffer).decode('utf-8')

class ResultsUploader(QObject):
    
    results_queue = queue.Queue(maxsize=10)
    
    def __init__(self):
        super().__init__()
        
        self._running = False
        
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._results_upload_thread)
        
    
    def _results_upload_thread(self):
        
        logger.info("Results uploader started.")
        self._running = True
        
        while self._running:
            if not self.results_queue.empty():
                frame, results = self.results_queue.get()
                
                # Prepare json data
                json_data = self._prepare_json_data(frame, results)
                
                # Upload the results
                try:
                    response = requests.post(
                        f"{SERVER_URL}/{RESULT_UPLOAD_ENDPOINT}",
                        json=json_data
                    )
                    response.raise_for_status()
                    logger.info(f"Results uploaded successfully: {response.status_code}")
                except requests.RequestException as e:
                    logger.error(f"Failed to upload results: {str(e)}")

    
    def _prepare_json_data(self, frame, results):
        
        datetime_now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        growth_stage_data = GrowthStageData(
            device_id=DEVICE_ID,
            timestamp=datetime_now,
            detections=[],  # Initialize detections
            image=ImageData(
                image_filename=f"{DEVICE_ID}_{datetime_now}.jpg",
                image_base64=encode_image_frame_to_base64(frame)
            )
        )
        
        for prediction in results.predictions:
            growth_stage_data.detections.append(
                Detection(
                    class_id=prediction.class_id,
                    class_name=prediction.class_name,
                    confidence=prediction.confidence,
                    class_confidence=prediction.class_confidence,
                    bounding_box=BoundingBox(
                        x_center=prediction.x,
                        y_center=prediction.y,
                        width=prediction.width,
                        height=prediction.height
                    )
                )
            )
            
        return growth_stage_data.model_dump()

    def start(self):
        if not self.thread.isRunning():
            self.thread.start()
        
    
    def stop(self):
        self._running = False
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        
        logger.info("Results uploader stopped.")