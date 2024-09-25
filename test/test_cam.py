import cv2

def main():
    # Initialize the video capture object with the default camera (0)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    # Optionally, set the width and height of the frames
    # Uncomment and adjust the values if needed
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Press 'q' to exit.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If frame reading was not successful, break the loop
        if not ret:
            print("Failed to grab frame.")
            break

        # Display the resulting frame in a window named 'Camera Feed'
        cv2.imshow('Camera Feed', frame)

        # Wait for 1 ms and check if 'q' key is pressed to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting...")
            break

    # Release the capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
