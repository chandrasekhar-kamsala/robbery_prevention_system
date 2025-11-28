import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pygame
import threading


class AlertSystem:
    def __init__(self, config):
        self.config = config
        # Initialize sound system only once
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"⚠️ Could not initialize sound system: {e}")

    def send_alert(self, message="Weapon detected!"):
        mode = self.config.get("alert_mode", "sound")

        if mode == "sound":
            print("🔔 Alert Triggered: Playing sound alert...")
            try:
                # Run in background so it doesn't block detection
                threading.Thread(target=self._play_sound, daemon=True).start()
            except Exception as e:
                print(f"⚠️ Could not play alert sound: {e}")

        elif mode == "email":
            print("📧 Sending alert email...")
            self._send_email(message)

        else:
            print("⚠️ Unknown alert mode in config.json")

    def _play_sound(self):
        """Play alert sound safely without alias issues."""
        try:
            pygame.mixer.music.load("alert.mp3")
            pygame.mixer.music.play()
        except Exception as e:
            print(f"⚠️ Could not play alert sound: {e}")

    def _send_email(self, message):
        """Send structured email alert."""
        sender = "nanikamsala2005@gmail.com"
        password = "nwbssygkimenswxn"  # Gmail App Password
        receiver = self.config.get("alert_email")
        subject = "Robbery Alert - Weapon Detected"

        try:
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = receiver
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain", "utf-8"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()

            print("✅ Email alert sent successfully!")

        except Exception as e:
            print(f"❌ Email sending failed: {e}")
