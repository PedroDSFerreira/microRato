import statistics
from collections import deque

BUFFER_SIZE = 3


class SensorBuffer:
    def __init__(self, sensor_count=4):
        self.buffers = [deque(maxlen=BUFFER_SIZE) for _ in range(sensor_count)]

    def add_sample(self, sensor_id, value):
        """Add a new sensor reading to the buffer."""
        self.buffers[sensor_id].append(value)

    def get_parsed_value(self, sensor_id, threshold=0.1):
        """Return the mean of the latest values, removing anomalies."""
        buffer = list(self.buffers[sensor_id])
        if len(buffer) == 0:
            return None

        mean_value = statistics.mean(buffer)

        # Remove values that deviate too much from the mean
        filtered_values = [v for v in buffer if abs(v - mean_value) <= threshold]

        if len(filtered_values) == 0:
            return mean_value  # Return mean if all values are considered anomalies
        return statistics.mean(filtered_values)
