from ultralytics import YOLO
import cv2
import shared_data

# After detecting and counting people


model = YOLO("yolov8n.pt")  # Use nano version for speed

def detect_people(frame):
    results = model(frame)
    people = 0
    centers = []

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            if model.names[cls] == 'person':
                people += 1
                xyxy = box.xyxy[0].tolist()
                center_x = int((xyxy[0] + xyxy[2]) / 2)
                center_y = int((xyxy[1] + xyxy[3]) / 2)
                centers.append((center_x, center_y))

                # Draw the bounding box
                cv2.rectangle(frame,
                              (int(xyxy[0]), int(xyxy[1])),
                              (int(xyxy[2]), int(xyxy[3])),
                              (0, 255, 0), 2)

    return frame, people, centers
