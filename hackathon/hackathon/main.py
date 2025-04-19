import cv2
import numpy as np
from ultralytics import YOLO
from camera_stream import get_camera_stream
from twilio.rest import Client
import threading
import time

# Load YOLOv8 face detection model (ensure it's available locally)
model = YOLO("yolov8n.pt")

# Face detection threshold
FACE_THRESHOLD = 5

# Twilio credentials (Replace with your own)
TWILIO_ACCOUNT_SID = 'ACa09c67ad762f5039ce229ea492c40af8'
TWILIO_AUTH_TOKEN = '79e10e19aad680c63e8603c4a521ce49'
TWILIO_FROM_NUMBER = '+14787788030'
ALERT_TO_NUMBER = '+916281629149'

# Alert cooldown
last_alert_time = 0
cooldown_seconds = 60

def send_sms_alert(current_count, threshold, cam_id):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f'⚠️ Crowd Alert (Camera {cam_id})! Detected {current_count} faces, exceeding threshold {threshold}.',
            from_=TWILIO_FROM_NUMBER,
            to=ALERT_TO_NUMBER
        )
        print(f"[ALERT SENT] Camera {cam_id} - SMS SID: {message.sid}")
    except Exception as e:
        print(f"[ALERT FAILED - Camera {cam_id}] {e}")

def send_alert(current_count, threshold, cam_id):
    global last_alert_time
    now = time.time()

    if now - last_alert_time < cooldown_seconds:
        return

    last_alert_time = now
    threading.Thread(target=send_sms_alert, args=(current_count, threshold, cam_id)).start()

def detect_faces_yolo(frame):
    results = model(frame)[0]
    boxes = results.boxes.xyxy.cpu().numpy().astype(int)
    count = 0

    for box in boxes:
        x1, y1, x2, y2 = box[:4]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        count += 1

    return frame, count

def draw_alert_border(frame):
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (w - 1, h - 1), (0, 0, 255), 10)

def main():
    stream1 = get_camera_stream(1)
    stream2 = get_camera_stream(2)

    while True:
        try:
            frame1 = next(stream1)
            frame2 = next(stream2)

            frame1, count1 = detect_faces_yolo(frame1)
            frame2, count2 = detect_faces_yolo(frame2)

            if count1 > FACE_THRESHOLD:
                draw_alert_border(frame1)
                send_alert(count1, FACE_THRESHOLD, 1)

            if count2 > FACE_THRESHOLD:
                draw_alert_border(frame2)
                send_alert(count2, FACE_THRESHOLD, 2)

            cv2.putText(frame1, f"Faces: {count1}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame2, f"Faces: {count2}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            height = min(frame1.shape[0], frame2.shape[0])
            frame1 = cv2.resize(frame1, (640, height))
            frame2 = cv2.resize(frame2, (640, height))
            combined = np.hstack((frame1, frame2))

            cv2.imshow("YOLO Face Detection – Dual Webcam", combined)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except StopIteration:
            break
        except Exception as e:
            print(f"[Error]: {e}")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
