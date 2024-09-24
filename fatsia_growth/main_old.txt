import os
import sys
import argparse
import cv2
import inference
import supervision as sv
import requests as req
from concurrent.futures import ThreadPoolExecutor
import queue
from datetime import datetime
from schemas.fatsia import GrowthStageData, Detection, BoundingBox, ImageData
import base64
import numpy as np
import threading
import logging

# Configuration
DEVICE_ID = "fatsia_cam_1"
ROBOFLOW_API_KEY = "7FfprDdtq5BKCbQSjE91"
SERVER_URL = "http://127.0.0.1:8000"
FATSIA_ROUTE = "fatsia/growth"

# Queues
send_queue = queue.Queue()
plot_queue = queue.Queue()

# Stop event
stop_event = threading.Event()

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def encode_frame_to_base64(frame):
    """Encodes a frame to a base64 string."""
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        logging.error("Could not encode frame to JPEG.")
        return None
    return base64.b64encode(buffer).decode('utf-8')

def get_image_and_inference_task(device_id, camera, model):
    """Captures images, performs inference, and queues the results."""
    while not stop_event.is_set():
        ret, frame = camera.read()
        if not ret:
            logging.error("Failed to capture image.")
            continue

        # Perform inference on the frame
        try:
            results = model.infer(frame)[0]
        except Exception as e:
            logging.error(f"Inference failed: {e}")
            continue

        datetime_now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        growth_stage_data = GrowthStageData(
            device_id=device_id,
            timestamp=datetime_now,
            detections=[],  # Initialize detections
            image=ImageData(
                image_filename=f"{device_id}_{datetime_now}.jpg",
                image_base64=encode_frame_to_base64(frame)
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

        send_queue.put(growth_stage_data)
        plot_queue.put(dict(
            image=frame,
            results=results
        ))

def send_results_task(server_url):
    """Sends inference results to the server."""
    while not stop_event.is_set():
        data_item = send_queue.get()
        if data_item is None:
            break

        try:
            response = req.post(f"{server_url}/{FATSIA_ROUTE}", json=data_item.dict())
            response.raise_for_status()
            logging.info(f"Data sent successfully: {response.status_code}")
        except req.exceptions.RequestException as e:
            logging.error(f"Failed to send data: {e}")
        finally:
            send_queue.task_done()

def show_results_task():
    """Displays the results using OpenCV."""
    while not stop_event.is_set():
        data_item = plot_queue.get()
        if data_item is None:
            break

        try:
            frame = data_item['image']
            results = data_item['results']

            detections = sv.Detections.from_inference(results)
            # create supervision annotators
            bounding_box_annotator = sv.BoxAnnotator()
            label_annotator = sv.LabelAnnotator()

            # annotate the image with our inference results
            annotated_image = bounding_box_annotator.annotate(scene=frame, detections=detections)
            annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

            # Display the resulting frame
            cv2.imshow('Camera Feed', annotated_image)
            cv2.waitKey(1)

        except Exception as e:
            logging.error(f"Exception while decoding and displaying image: {e}")
        finally:
            plot_queue.task_done()

def cleanup():
    """Cleans up resources and signals threads to stop."""
    stop_event.set()
    send_queue.put(None)
    plot_queue.put(None)
    logging.info("Cleanup complete. Resources released.")

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--device_id", type=str, default=DEVICE_ID)
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--model_id", type=str, default="fatsia_growth_stages/4")
    parser.add_argument("--api_key", type=str, default=ROBOFLOW_API_KEY)
    args = parser.parse_args()

    # Initialize
    device_id = args.device_id
    camera = cv2.VideoCapture(args.camera)
    model = inference.get_model(
        model_id=args.model_id,
        api_key=args.api_key
    )

    if not camera.isOpened():
        logging.error("Could not open camera.")
        sys.exit(1)

    try:
        # Start the thread pool
        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(get_image_and_inference_task, device_id, camera, model)
            executor.submit(send_results_task, SERVER_URL)
            executor.submit(show_results_task)

            # Wait for stop signal
            while not stop_event.is_set():
                pass

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received. Exiting...")
    finally:
        cleanup()
        camera.release()
        cv2.destroyAllWindows()
        logging.info("Program terminated.")
