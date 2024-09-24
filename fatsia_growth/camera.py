import cv2


class Camera:
    def __init__(self, camera_id=0):
        """
        Initialize the Camera with the given camera_id.

        Args:
            camera_id (int): The ID of the camera to use.
        """
        self.camera_id = camera_id
        self.cap = None
        self.is_opened = False

    def open(self):
        """Open the camera."""
        self.cap = cv2.VideoCapture(self.camera_id)
        if self.cap.isOpened():
            self.is_opened = True
        else:
            self.is_opened = False

    def read_frame(self):
        """
        Read a single frame from the camera.

        Returns:
            frame (numpy.ndarray or None): The captured frame or None if failed.
        """
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def release(self):
        """Release the camera resource."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.is_opened = False