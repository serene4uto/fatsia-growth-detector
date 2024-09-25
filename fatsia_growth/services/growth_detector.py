import queue

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
import inference

from fatsia_growth.utils.logger import logger

ROBOFLOW_API_KEY = "7FfprDdtq5BKCbQSjE91"
ROBOFLOW_MODEL_IDS = [
    "fatsia_growth_stages/4",
]

def get_roboflow_model_ids():
    return ROBOFLOW_MODEL_IDS

class GrowthDetector(QObject):
    
    frame_queue = queue.Queue(maxsize=10)
    
    def __init__(
        self
    ):
        super().__init__()
        
        self.rbf_api_key = ROBOFLOW_API_KEY
        self.rbf_model_id = None
        self.rbf_model = None
        
        self._running = False
        
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._detector_thread)
        
    def _detector_thread(self):
        try:
            self.rbf_model = inference.get_model(
                model_id = self.rbf_model_id,
                api_key = self.rbf_api_key
            )
            
            if self.rbf_model is not None:
                logger.info(f"Model {self.rbf_model_id} loaded successfully.")
                self._running = True
                while self._running:
                    if not self.frame_queue.empty():
                        frame = self.frame_queue.get()
                        result = self.rbf_model.infer(frame)[0]
                        logger.info(f"Prediction result: {result}")
                        
            else:
                logger.error(f"Model {self.rbf_model_id} could not be loaded.")
                self.stop()
            
        except Exception as e:
            logger.error(f"Exception in detector thread: {e}")
            self.stop()
        
        
    def start(self, model_id):
        self.rbf_model_ids = model_id
        if not self.thread.isRunning():
            self.thread.start()
    
    def stop(self):
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
            
        self.rbf_model_id = None
        self.rbf_model = None
    
    # @pyqtSlot(object)
    # def on_frame_captured(self, frame):
    #     logger.info("Frame added to queue.")
    #     # self.frame_queue.put(frame)
        
        