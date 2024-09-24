from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage
import cv2


class CameraWorker(QObject):
    """
    Worker class to handle camera operations in a separate thread.
    """
    frame_received = pyqtSignal(QImage)
    error = pyqtSignal(str)

    def __init__(self, camera):
        """
        Initialize the CameraWorker.

        Args:
            camera (Camera): An instance of the Camera class.
        """
        super().__init__()
        self.camera = camera
        self._is_running = True

    # def start_camera(self):
    #     """Start capturing frames from the camera."""
    #     self.camera.open()
    #     if not self.camera.is_opened:
    #         self.error.emit("Unable to access the camera.")
    #         return

    #     while self._is_running:
    #         frame = self.camera.read_frame()
    #         if frame is None:
    #             self.error.emit("Failed to grab frame.")
    #             break

    #         # Convert frame to RGB
    #         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         height, width, channel = rgb_frame.shape
    #         bytes_per_line = 3 * width

    #         # Create QImage from frame
    #         q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

    #         # Emit the signal with the new frame
    #         self.frame_received.emit(q_image)

    #     # Release the camera when done
    #     self.camera.release()

    # def stop(self):
    #     """Stop capturing frames."""
    #     self._is_running = False