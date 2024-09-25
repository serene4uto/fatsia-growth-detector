import cv2

def get_available_cameras(max_cameras=10):
    """
    Detect available cameras by attempting to open camera indices up to max_cameras.

    Args:
        max_cameras (int): Maximum number of camera indices to check.

    Returns:
        list of camera indices that are available.
    """
    available_cameras = []
    for camera_id in range(max_cameras):
        cap = cv2.VideoCapture(camera_id)
        if cap is not None and cap.isOpened():
            available_cameras.append(camera_id)
            cap.release()
    return available_cameras