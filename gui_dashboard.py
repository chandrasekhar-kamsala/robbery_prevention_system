import cv2
import json
import time
import threading
import tkinter as tk
from tkinter import Label, Button, Frame, Text, Scrollbar, END
from PIL import Image, ImageTk
from detector import WeaponDetector
from alert_system import AlertSystem
from power_monitor import PowerMonitor


class RobberyPreventionGUI:
    def __init__(self, master):
        self.master = master
        master.title("🛡️ Robbery Prevention System")
        master.geometry("1300x750")
        master.configure(bg="#0b0c10")

        # Load Config
        with open("config.json", "r") as f:
            self.config = json.load(f)

        # Initialize components
        self.detector = WeaponDetector(self.config["model_path"])
        self.alert = AlertSystem(self.config)
        self.power_monitor = PowerMonitor(self.config.get("power_check_interval", 10))
        self.running = False

        # --- HEADER ---
        header = Frame(master, bg="#1f2833", height=60)
        header.pack(fill="x")
        Label(header, text="🛡️ Robbery Prevention & Smart Alert System",
              bg="#1f2833", fg="#66fcf1",
              font=("Helvetica", 20, "bold")).pack(pady=10)

        # --- VIDEO FRAME ---
        video_frame = Frame(master, bg="#1f2833")
        video_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.video_label = Label(video_frame, bg="#000000")
        self.video_label.pack(fill="both", expand=True)

        # Overlay alert banner
        self.alert_banner = Label(video_frame, text="", bg="red", fg="white",
                                  font=("Arial", 16, "bold"), pady=5)
        self.alert_banner.place(relx=0.5, rely=0.05, anchor="center")
        self.alert_banner.lower()

        # --- CONTROL PANEL ---
        control_panel = Frame(master, bg="#1f2833", width=350)
        control_panel.pack(side="right", fill="y")

        Label(control_panel, text="⚙️ System Controls", bg="#1f2833",
              fg="#ffffff", font=("Arial", 16, "bold")).pack(pady=10)

        self.status_label = Label(control_panel, text="Status: 🟥 Stopped",
                                  bg="#1f2833", fg="red", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=5)

        self.power_label = Label(control_panel, text="⚡ Power: Checking...",
                                 bg="#1f2833", fg="yellow", font=("Arial", 14, "bold"))
        self.power_label.pack(pady=5)

        self.alert_label = Label(control_panel, text="🔔 Alerts: None",
                                 bg="#1f2833", fg="#45a29e", font=("Arial", 14, "bold"))
        self.alert_label.pack(pady=10)

        self.start_btn = Button(control_panel, text="▶ Start System", command=self.start_system,
                                bg="#45a29e", fg="white", font=("Arial", 12, "bold"),
                                relief="flat", width=20)
        self.start_btn.pack(pady=10)

        self.stop_btn = Button(control_panel, text="⏹ Stop System", command=self.stop_system,
                               bg="#c3073f", fg="white", font=("Arial", 12, "bold"),
                               relief="flat", width=20)
        self.stop_btn.pack(pady=5)

        Label(control_panel, text="📜 Live System Logs", bg="#1f2833",
              fg="white", font=("Arial", 15, "bold")).pack(pady=10)

        self.log_box = Text(control_panel, height=22, width=45,
                            bg="#0b0c10", fg="white", wrap="word",
                            font=("Consolas", 11))
        self.log_box.pack(padx=10, pady=5)

        scrollbar = Scrollbar(control_panel, command=self.log_box.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_box['yscrollcommand'] = scrollbar.set

        # Camera Setup
        self.cap = cv2.VideoCapture(self.config.get("camera_index", 0))

    # ------------------ Utility Functions ------------------ #
    def log(self, message, color="white"):
        timestamp = time.strftime("%H:%M:%S")
        self.log_box.insert(END, f"[{timestamp}] {message}\n", color)
        self.log_box.tag_config(color, foreground=color)
        self.log_box.see(END)

    def show_banner(self, text, color="red"):
        """Show temporary banner on video feed"""
        self.alert_banner.config(text=text, bg=color)
        self.alert_banner.lift()
        self.master.after(3000, lambda: self.alert_banner.lower())

    def start_system(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="Status: 🟩 Running", fg="lime")
            self.alert_label.config(text="🔔 Alerts: Monitoring...", fg="#66fcf1")
            self.log("✅ System Started.", "lime")
            self.show_banner("✅ System Started", "#45a29e")
            threading.Thread(target=self.run_detection, daemon=True).start()
        else:
            self.log("⚠️ System already running.", "yellow")

    def stop_system(self):
        self.running = False
        self.status_label.config(text="Status: 🟥 Stopped", fg="red")
        self.alert_label.config(text="🔔 Alerts: None", fg="#45a29e")
        self.log("🛑 System Stopped.", "red")
        self.show_banner("🛑 System Stopped", "#c3073f")

    def blink_alert(self):
        """Blink alert label during detection"""
        if not self.running:
            return
        current_color = self.alert_label.cget("fg")
        next_color = "white" if current_color == "red" else "red"
        self.alert_label.config(fg=next_color)
        self.master.after(400, self.blink_alert)

    # ------------------ Core Logic ------------------ #
    def run_detection(self):
        last_power_check = time.time()

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                self.log("⚠️ Camera feed lost! Possible power issue.", "red")
                self.alert.send_alert("Camera feed lost! Possible power outage.")
                self.show_banner("⚠️ Camera Feed Lost!", "orange")
                break

            annotated_frame, detections = self.detector.detect(frame, self.config["confidence_threshold"])
            img = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)

            # Weapon Detection
            if len(detections) > 0:
                self.log(f"🚨 Weapon Detected: {detections}", "red")
                self.alert_label.config(text="🚨 ALERT: Weapon Detected!", fg="red")
                self.blink_alert()
                self.show_banner("🚨 WEAPON DETECTED!", "red")
                self.alert.send_alert("Weapon detected in surveillance area!")

                # Display alert type feedback
                if self.config.get("alert_mode") == "sound":
                    self.show_banner("🔊 Sound Alert Triggered!", "#1f2833")
                elif self.config.get("alert_mode") == "email":
                    self.show_banner("📧 Alert Email Sent!", "#1f2833")

                time.sleep(2)
                self.alert_label.config(text="🔔 Alerts: Monitoring...", fg="#66fcf1")

            # Power Check
            if time.time() - last_power_check >= self.config.get("power_check_interval", 10):
                status = self.power_monitor.run()
                color = "green" if status == "OK" else "red"
                self.power_label.config(text=f"⚡ Power: {status}", fg=color)
                if status == "OUTAGE":
                    self.log("⚡ Power outage detected!", "yellow")
                    self.show_banner("⚡ POWER OUTAGE DETECTED!", "orange")
                    self.alert.send_alert("⚡ Power outage detected! Check security line.")
                last_power_check = time.time()

        self.cap.release()
        self.status_label.config(text="Status: 🟥 Stopped", fg="red")
        self.log("👋 System stopped cleanly.", "white")
        self.show_banner("👋 System Stopped Cleanly", "#1f2833")


# ------------------ Run GUI ------------------ #
if __name__ == "__main__":
    root = tk.Tk()
    app = RobberyPreventionGUI(root)
    root.mainloop()
