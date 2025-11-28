import time
import random

class PowerMonitor:
    def __init__(self, check_interval=10):
        """check_interval: seconds between each simulated power check"""
        self.interval = check_interval
        self.last_check = time.time()

    def check_status(self):
        """Randomly simulate power states"""
        status = random.choice(["OK", "FLUCTUATION", "OUTAGE"])
        print(f"⚡ Power Status: {status}")
        return status

    def run(self):
        """Return one power status check — non-blocking"""
        # only check if interval time has passed
        if time.time() - self.last_check >= self.interval:
            self.last_check = time.time()
            return self.check_status()
        return "OK"  # default normal state
