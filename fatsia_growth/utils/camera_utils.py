import cv2

def get_available_cameras(max_cameras=10):
    """
    Detect available cameras by attempting to open camera indices up to max_cameras.

    Args:
        max_cameras (int): Maximum number of camera indices to check.

    Returns:
        list of tuples: Each tuple contains (camera_id, camera_name)
    """
    available_cameras = []
    for camera_id in range(max_cameras):
        cap = cv2.VideoCapture(camera_id)
        if cap is not None and cap.isOpened():
            camera_name = f"Camera {camera_id}"
            available_cameras.append((camera_id, camera_name))
            cap.release()
    return available_cameras