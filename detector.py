from ultralytics import YOLO
import cv2

class WeaponDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame, conf_threshold=0.4):
        results = self.model(frame)
        annotated_frame = results[0].plot()
        detections = []
        for box in results[0].boxes:
            if box.conf[0] >= conf_threshold:
                cls = int(box.cls[0])
                name = results[0].names[cls]
                conf = float(box.conf[0])
                detections.append({"class": name, "confidence": conf})
        return annotated_frame, detections
