# LiveFlow AI

LiveFlow AI is an AI-powered dual-camera crowd monitoring and face detection system using YOLOv8, integrated with Twilio SMS alerting and real-time threshold-based detection. It provides a dashboard-style visualization and sends alerts when the detected face count exceeds a set threshold.

## 🚀 Features
- 📷 Real-time face detection using YOLOv8 from two USB webcams.
- ⚠️ Threshold-based crowd alerts with visual red borders.
- 📲 Instant SMS alerts using Twilio when face count exceeds the defined limit.
- 🧠 Extendable anomaly detection and heatmap functionality.
- 🛡️ Modular and scalable code structure with OpenCV and Ultralytics YOLO.

## 🧰 Tech Stack
- Python 3.9+
- OpenCV
- Ultralytics YOLOv8
- Twilio API (for SMS alerts)
- NumPy
- Flask (for web interface if needed)
- SQLite / SQLPlus (for optional logging)
- Two external USB webcams

## 📦 Folder Structure
```
LiveFlowAI/
│
├── main.py                   # Main execution script
├── camera_stream.py          # Handles webcam stream
├── crowd_detector.py         # YOLOv8 face detection logic
├── alert_system.py           # Twilio alert integration
├── database.py               # Logs count into DB (optional)
├── heatmap_generator.py      # (Optional) For heatmap visualization
├── anomaly_detector.py       # (Optional) Detects sudden anomalies
├── requirements.txt          # Python dependencies
```

## ⚙️ How it works
1. Captures real-time video from two webcams.
2. YOLOv8 detects faces from both feeds.
3. If face count > threshold (default = 5), red alert border is shown.
4. Sends SMS alert via Twilio API.
5. Logs detection count to the database (optional).

## 🔔 Twilio SMS Alert Format
```
⚠️ Crowd Alert! Current count is {count}, which exceeds the threshold {threshold}.
```

## ✅ Setup Instructions
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Connect two USB webcams or any other camera with help of ip address.
4. Replace Twilio credentials in `alert_system.py`.
5. Run the project: `python main.py`

## 🧪 Future Scope
- Web-based admin dashboard to visualize live feed and analytics.
- Email alert integration with logs.
- Face recognition and blacklist matching.
- Heatmap overlay using crowd density.
- Cloud deployment support.

## 🤝 Contribution
Pull requests are welcome. For major changes, please open an issue first.

## Team Members:
L Pravena - praveenalanda@gmail.com
K. Jayanth - jayanth.kapudasu@gmail.com
K. Thanuj Kumar - kumarthanuj76@gmail.com

## 📝 License
This project is open-source and free to use under the MIT License.
