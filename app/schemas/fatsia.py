from pydantic import BaseModel, Field
from typing import List, Union

class BoundingBox(BaseModel):
    x_center: float
    y_center: float
    width: float
    height: float

class Detection(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    class_confidence: Union[float, None]
    bounding_box: BoundingBox

class ImageData(BaseModel):
    image_filename: str
    image_base64: str  # Base64 encoded image data as a string

class GrowthStageData(BaseModel):
    device_id: str
    timestamp: str
    detections: List[Detection]
    image: ImageData  # Add image data to the model
