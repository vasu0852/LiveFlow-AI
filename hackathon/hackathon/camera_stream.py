import cv2

def get_camera_stream(source=0):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise Exception(f"[!] Failed to open camera source: {source}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield frame

    cap.release()
