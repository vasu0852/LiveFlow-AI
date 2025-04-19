import time

class AnomalyDetector:
    def __init__(self):
        self.last_count = 0
        self.last_time = time.time()
        self.spike_threshold = 5  # Number of people
        self.time_threshold = 5   # Seconds

    def check_for_anomaly(self, current_count):
        current_time = time.time()
        count_diff = current_count - self.last_count
        time_diff = current_time - self.last_time

        self.last_count = current_count
        self.last_time = current_time

        if count_diff >= self.spike_threshold and time_diff <= self.time_threshold:
            return True
        return False

