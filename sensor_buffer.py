import statistics
from collections import deque

BUFFER_SIZE = 2  # Fixed buffer size of 2
THRESHOLD = 0.7  # Threshold for anomaly detection


class SensorBuffer:
    def __init__(self, sensor_count=4):
        self.buffers = [deque(maxlen=BUFFER_SIZE) for _ in range(sensor_count)]

    def add(self, sensor_id, value):
        """Add a new sensor reading to the buffer."""
        self.buffers[sensor_id].append(value)

    def get(self, sensor_id):
        """Return the median of the last two values if they're close, otherwise the previous value."""
        buffer = list(self.buffers[sensor_id])
        if len(buffer) < 2:
            return buffer[0] if buffer else None

        previous_value, current_value = buffer

        # If the values deviate too much, return the previous value
        if abs(current_value - previous_value) > THRESHOLD:
            return previous_value

        # If the values are close, return the median
        return statistics.median(buffer)
