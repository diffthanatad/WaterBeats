from datetime import datetime as dt
import datetime
import os
import random
from math import sin
import requests


class SensorDataGenerator:
    def __init__(self) -> None:
        self.sensor_id = "test_sensor_1"
        self.sensor_type = "temperature"
        self.unit = "C"
        self.longitude = 123.1
        self.latitude = -42.0
        self.timestamp = dt.fromtimestamp(1641773400)
        self.data_y = 20
        self.data_x = 0
        self.data_amplitude = 3
        self.data_x_delta = 0.03
        self.data_y_inc = 0.5

    def __next__(self):
        self.timestamp += datetime.timedelta(minutes=10)
        self.data_y = (
            random.uniform(0, self.data_amplitude) * sin(self.data_x)
            + 20
            + random.uniform(-1, 1)
            + self.data_y_inc
        )
        self.data_x += self.data_x_delta
        self.data_y_inc += 0.01
        return {
            "sensor_id": self.sensor_id,
            "sensor_type": self.sensor_type,
            "unit": self.unit,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "timestamp": self.timestamp,
            "data": self.data_y,
        }


gen = SensorDataGenerator()
data = []
for i in range(1000):
    d = next(gen)
    data.append(d)

# save data to influxdb
data_lines = map(
    lambda x: f'sensor_data,sensor_id={x["sensor_id"]},sensor_type={x["sensor_type"]} unit="{x["unit"]}",longitude={x["longitude"]},latitude={x["latitude"]},data={x["data"]} {int(x["timestamp"].timestamp() * 1e9)}',
    data,
)
payload = "\n".join(data_lines)
print(payload)

token = os.environ["INFLUXDB_TOKEN"]
r = requests.post(
    "http://localhost:8086/api/v2/write?org=WaterBeats&bucket=WaterBeats&precision=ns",
    data=payload,
    headers={
        "Authorization": f"Token {token}",
    },
)
if r.status_code != 204:
    print("Error writing to InfluxDB")
    print(r.text)
