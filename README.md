# 🔫 Robbery Prevention & Smart Alert System  
### Real-Time Weapon Detection | Smart Alerts | YOLOv8 + OpenCV + Tkinter

A real-time security surveillance application that detects weapons (Handgun, Shotgun, Knife, etc.) using **YOLOv8**, displays alerts on a **Tkinter dashboard**, and triggers **email + sound alerts** instantly.  
Also features a **power monitoring system** that simulates outages and triggers emergency warnings.

---

## 🚀 Features

- ⚡ **Real-Time Weapon Detection** using YOLOv8  
- 🖥 **Interactive Tkinter GUI Dashboard**  
- 📢 **Sound Alerts** when a weapon is detected  
- 📧 **Email Notifications (SMTP)**  
- 📊 **Live System Logs** with timestamps  
- 🔌 **Power Monitoring System** (OK, OUTAGE, FLUCTUATION)  
- 🧵 **Multithreading** for smooth real-time processing  
- 💾 **JSON configuration** for editable settings  
- 🎥 Works with webcam OR video files  

---

## 📁 Folder Structure
WEAPONDETECTION/
│── alert_system.py
│── alert.mp3
│── config.json
│── detector.py
│── gui_dashboard.py
│── main.py
│── power_monitor.py
│── requirements.txt
│── test_video.mp4
│── test_video1.mp4
│── weapon_yolov8.pt <-- Your trained weights
│── screenshots/ <-- Add your images here
└── .gitignore
---

## 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| Model | YOLOv8 |
| Framework | OpenCV |
| GUI | Tkinter |
| Alerts | SMTP + Pygame |
| Language | Python |
| Utils | Threading, JSON, Logging |

---

## 📷 Screenshots  

> Upload your images into a folder named **screenshots/** in your repo  
> Then rename them to match these:

### 🔹 **Weapon Detection (YOLOv8 Output)**
![Weapon Detection](screenshots/weapon-detection-1.png)

### 🔹 **Main Dashboard (Stopped State)**
![Dashboard Stopped](screenshots/dashboard-stopped.png)

### 🔹 **Running System – Weapon Detected**
![Weapon Detected](screenshots/weapon-detected.png)

### 🔹 **Sound Alert Triggered**
![Sound Trigger](screenshots/sound-alert.png)

### 🔹 **Power Outage Notification**
![Power Outage](screenshots/power-outage.png)

### 🔹 **Email Alert Sent**
![Email Alert](screenshots/email-alert.png)

---

# Robbery Prevention System - Setup Guide

📦 **Installation**
steps:
  - **Clone the Repository**
    command: |
      git clone https://github.com/your-username/Robbery-Prevention-System.git
      cd Robbery-Prevention-System
  - **Install Dependencies**
    command: "pip install -r requirements.txt"
  - **Add Your YOLOv8 Weights**
    instructions: "Place your trained YOLO model file in the project root directory"
    file: "weapon_yolov8.pt"

▶️ **Usage**
start_system: "python main.py"
controls:
  - **Start System**: "Starts webcam/video detection"
  - **Stop System**: "Stops detection"
  - **Live Logs**: "Shows real-time alerts"
  - **Power Alerts**: "Displays outage, fluctuation, OK statuses"

⚙️ **Configuration**
config_file: "config.json"
settings:
  use_webcam: false
  video_path: "test_video.mp4"
  confidence_threshold: 0.45
  email_sender: "your_email@gmail.com"
  email_receiver: "receiver@gmail.com"

📬 **Email Alert Setup**
steps:
  - "Enable Gmail App Passwords"
  - "Replace credentials in config.json"
  - "Ensure your sender email has 2FA enabled"

🤖 **YOLOv8 Model**
description: "This project uses your custom-trained model"
file: "weapon_yolov8.pt"
note: "You can replace it anytime with a newer YOLOv8 weight file"

📚 **Future Enhancements**
  - "Cloud-based analytics dashboard"
  - "Multi-camera support"
  - "SMS/WhatsApp alert system"
  - "Raspberry Pi deployment"
  - "CCTV DVR/NVR pipeline integration"

⭐ **Show Your Support**
message: "If this project helped you or impressed you, consider giving it a ⭐ on GitHub! 🙌"
