# 😷 AI Mask Detection System using YOLOv8 & Flask

An intelligent real-time face mask detection and monitoring system built with **YOLOv8**, **Flask**, and **OpenCV**.  
The application detects whether a person is wearing a mask through a webcam stream, triggers audio alerts for violations, automatically stores evidence images, and provides an interactive web dashboard for monitoring and reporting.

---

# 📌 Overview

This project was developed to support automated safety monitoring in environments such as:

- Schools
- Universities
- Offices
- Public facilities
- Smart surveillance systems

The system utilizes a custom-trained **YOLOv8 model** to classify:

- 😷 Mask
- ❌ No Mask

Detection results are processed in real time and displayed directly through a web-based dashboard.

---

# ✨ Key Features

## 🎥 Real-Time Face Mask Detection
- Live webcam monitoring using a custom YOLOv8 model (`best.pt`)
- Real-time object detection with bounding boxes
- Color-based visualization:
  - 🟢 Green → Mask Detected
  - 🔴 Red → No Mask Detected

---

## 🔊 Intelligent Audio Warning System
- Automatically plays warning sounds when a violation is detected
- Cooldown mechanism prevents continuous repetitive alerts
- Configurable sound interval

---

## 📷 Automatic Violation Evidence Capture
- Automatically captures and stores violation images
- Images are saved into:

```bash
static/violations/
```

- Useful for monitoring, logging, and future analysis

---

## 📊 Interactive Web Dashboard
The dashboard includes:

- Live camera stream
- Total Mask / No Mask statistics
- Real-time pie chart visualization
- Violation logs table
- Evidence image preview
- CSV report export functionality

---

## 🔐 Admin Authentication
- Secure login system for administrators
- Restricts unauthorized access to the monitoring dashboard

---

## 📥 CSV Report Export
- Export all violation records into `.csv` format
- Compatible with Microsoft Excel and Google Sheets

---

# 🖼️ System Architecture

```text
Webcam
   │
   ▼
YOLOv8 Detection Model
   │
   ├── Mask Detection
   ├── No Mask Detection
   │
   ▼
Flask Backend Server
   │
   ├── Audio Alert
   ├── Save Violation Images
   ├── Update Dashboard
   └── Export Reports
```

---

# 🗂️ Project Structure

```bash
mask-detection/
│
├── app.py
├── detect.py
├── best.pt
├── requirements.txt
│
├── sounds/
│   └── Beep.mp3
│
├── static/
│   ├── styles.css
│   └── violations/
│
└── templates/
    ├── login.html
    ├── dashboard.html
    └── index.html
```

---

# 📁 File Descriptions

| File / Folder | Description |
|---|---|
| `app.py` | Main Flask application |
| `detect.py` | Standalone detection script |
| `best.pt` | Custom-trained YOLOv8 model |
| `requirements.txt` | Required Python libraries |
| `sounds/Beep.mp3` | Alert sound |
| `static/violations/` | Stored violation images |
| `templates/` | HTML templates |

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/mask-detection.git
cd mask-detection
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Prepare Required Files

Make sure the following files exist:

```bash
mask-detection/
├── best.pt
├── sounds/
│   └── Beep.mp3
```

---

# 🚀 Running the Application

# 🌐 Flask Web Dashboard Mode

```bash
python app.py
```

Open your browser and visit:

```bash
http://127.0.0.1:5000
```

---

## 🔑 Default Login Credentials

| Username | Password |
|---|---|
| admin | 123456 |

---

# 💻 Standalone Detection Mode

```bash
python detect.py
```

### Features:
- Runs detection without Flask
- Press `Q` to exit
- Automatically exports:

```bash
bao_cao_vi_pham.csv
```

---

# 📊 Dashboard Features

The monitoring dashboard provides:

✅ Live Camera Streaming  
✅ Detection Statistics  
✅ Pie Chart Visualization  
✅ Violation Logs  
✅ Image Evidence Management  
✅ CSV Report Download  

---

# 🛠️ Technologies Used

| Component | Technology |
|---|---|
| AI Detection Model | YOLOv8 (Ultralytics) |
| Backend Framework | Flask |
| Computer Vision | OpenCV |
| Data Processing | Pandas |
| Frontend Charts | Chart.js |
| Audio Processing | Pygame |
| Programming Language | Python |

---

# ⚡ Detection Workflow

1. Webcam captures video frames
2. YOLOv8 processes each frame
3. System detects:
   - Mask
   - No Mask
4. If violation detected:
   - Play alert sound
   - Save violation image
   - Update dashboard
   - Record violation logs
5. Data can be exported into CSV reports

---

# 📸 Detection Preview

## Mask Detected
- Green bounding box
- Label: `Mask`

## No Mask Detected
- Red bounding box
- Label: `No Mask`
- Audio warning activated
- Violation image stored automatically

---

# ⚠️ Important Notes

- The system uses the default webcam:

```python
cv2.VideoCapture(0)
```

Change the index if multiple cameras are connected.

---

- Detection accuracy improves significantly under good lighting conditions.

---

- `total_mask` and `total_nomask` are counted per detection frame, not per unique individual.

---

- If the alert sound file is missing, the system will continue operating silently.

---

# 🔮 Future Improvements

Possible future enhancements include:

- 📡 IP Camera / CCTV integration
- ☁️ Cloud database support
- 📱 Telegram or Email notifications
- 👥 Multi-person tracking
- 🧠 Face Recognition integration
- 📈 Advanced analytics dashboard
- 🏢 Enterprise deployment support

---

# 📚 Requirements

Example dependencies:

```txt
flask
opencv-python
ultralytics
pygame
pandas
numpy
```

---

# 📄 License

This project is released under the MIT License.

---

# 🙌 Contributions

Contributions are welcome!

Feel free to:
- Open Issues
- Submit Pull Requests
- Suggest Improvements
- Report Bugs

---

# ⚠️ Disclaimer

This project is developed for educational, research, and monitoring purposes only.  
It is not intended to replace official medical procedures or public health regulations.

---

# 👨‍💻 Author

Nguyen Manh Duc
Faculty of Information Technology
