import cv2
import json
import time
from detector import WeaponDetector
from alert_system import AlertSystem
from power_monitor import PowerMonitor

# ------------------------------
# Load Configuration
# ------------------------------
with open("config.json", "r") as f:
    config = json.load(f)

# ------------------------------
# Initialize Components
# ------------------------------
detector = WeaponDetector(config["model_path"])
alert = AlertSystem(config)
power_monitor = PowerMonitor(config.get("power_check_interval", 10))

# ------------------------------
# Open Webcam
# ------------------------------
cap = cv2.VideoCapture(config.get("camera_index",0))
if not cap.isOpened():
    print("❌ Could not access camera.")
    exit()

print("✅ Robbery Prevention System Active. Press 'q' to quit.")

last_power_check = time.time()

# ------------------------------
# Main Loop
# ------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Frame not received.")
        break

    # Weapon Detection
    annotated_frame, detections = detector.detect(frame, config["confidence_threshold"])
    cv2.imshow("Robbery Prevention System", annotated_frame)

    # Alert on weapon detection
    if len(detections) > 0:
        print("🚨 Weapon Detected:", detections)
        alert.send_alert("Weapon detected in surveillance area!")
        time.sleep(2)

    # Power Monitoring (periodic check)
    if time.time() - last_power_check >= config.get("power_check_interval", 10):
        status = power_monitor.check_status()
        last_power_check = time.time()

        if status == "OUTAGE":
            print("🔒 Power Outage Detected - Simulating Door Lockdown.")
            alert.send_alert("Power outage detected! System entering lockdown mode.")

    # Quit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ------------------------------
# Cleanup
# ------------------------------
cap.release()
cv2.destroyAllWindows()
print("👋 System stopped.")
