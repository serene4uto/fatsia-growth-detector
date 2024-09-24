import cv2
import logging

class Camera:
    """
    A class to encapsulate camera operations using OpenCV.
    """

    def __init__(self, camera_index=0):
        """
        Initialize the camera.

        :param camera_index: The index of the camera to use.
        """
        self.camera_index = camera_index
        self.camera = cv2.VideoCapture(self.camera_index)
        if not self.camera.isOpened():
            logging.error(f"Could not open camera with index {self.camera_index}.")
            raise ValueError(f"Camera with index {self.camera_index} could not be opened.")

    def read_frame(self):
        """
        Reads a frame from the camera.

        :return: The captured frame, or None if capture failed.
        """
        ret, frame = self.camera.read()
        if not ret:
            logging.error("Failed to capture image from camera.")
            return None
        return frame

    def release(self):
        """
        Releases the camera resource.
        """
        if self.camera.isOpened():
            self.camera.release()
            logging.info("Camera released successfully.")