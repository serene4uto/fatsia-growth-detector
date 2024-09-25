import cv2
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

class CameraService(QObject):
    
    camera_connection_changed = pyqtSignal(bool)
    frame_captured = pyqtSignal(object)
       
    def __init__(self):
        super().__init__()
        self.camera_id = None
        self.cap = None
        self._running = False

        self.thread = QThread()  # Create a new QThread instance
        self.moveToThread(self.thread)  # Move the CameraService to the new thread
        
        # Connect the thread's started signal to the camera thread method
        self.thread.started.connect(self._camera_thread)
        
    def _camera_thread(self):
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            if self.cap.isOpened():
                self.camera_connection_changed.emit(True)
                self._running = True
                while self._running:
                    ret, frame = self.cap.read()
                    if ret:
                        self.frame_captured.emit(frame)
            else:
                # Camera could not be opened, emit signal with -1
                self.camera_connection_changed.emit(False)
                self.stop()
        except Exception as e:
            print(f"Exception in camera thread: {e}")
            self.stop()

    def start(self, camera_id):
        self.camera_id = camera_id
        if not self.thread.isRunning():
            self.thread.start()  # Start the thread to begin capturing frames
    
    def stop(self):
        self._running = False
        self.camera_id = None
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None
        
        if self.thread.isRunning():
            self.thread.quit()  # Ask the thread to quit
            self.thread.wait()  # Wait for the thread to finish
        
        self.camera_connection_changed.emit(False)
