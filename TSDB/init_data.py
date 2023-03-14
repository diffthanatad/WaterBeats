from datetime import datetime as dt
import datetime
import os
import random
from math import sin
from typing import Tuple
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8086")
class SensorDataGenerator:
    def __init__(
        self,
        sensor_id: str,
        sensor_type: str,
        unit: str,
        coordinates: Tuple[float, float],
    ) -> None:
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.unit = unit
        (self.latitude, self.longitude) = coordinates
        # 1641773400 is 2022-01-10T00:10:00Z
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
            "status": ["on", "off", "error"][random.randint(0, 2)]
        }


data = []
for generator_args in [
    ("test_sensor_0", "temperature", "F", (55.16870067313674, -2.4134985245000102)),
    ("test_sensor_1", "temperature", "C", (55.169293309649646, -2.412925235580431)),
    ("test_sensor_2", "soil_moisture", "%", (55.16909847122022, -2.4127925736816853)),
    ("test_sensor_3", "water_level", "mm", (55.169358255581216, -2.4111200861725)),
    (
        "test_sensor_4",
        "water_pollution",
        "ppm",
        (55.16843005992712, -2.412110312488137),
    ),
]:
    data_generator = SensorDataGenerator(*generator_args)
    for i in range(1000):
        d = next(data_generator)
        data.append(d)

# save data to influxdb
data_lines = map(
    lambda x: f'sensor_data,sensor_id={x["sensor_id"]},sensor_type={x["sensor_type"]} unit="{x["unit"]}",longitude={x["longitude"]},latitude={x["latitude"]},data={x["data"]},status="{x["status"]}" {int(x["timestamp"].timestamp() * 1e9)}',
    data,
)
payload = "\n".join(data_lines)

actuator_data_lines = map(
    lambda x: f'actuator_data,actuator_id={x["actuator_id"]},actuator_type={x["actuator_type"]} status="{x["status"]}",longitude={x["longitude"]},latitude={x["latitude"]} {int(x["timestamp"].timestamp() * 1e9)}',
    [
        {
            "actuator_id": "test_actuator_1",
            "actuator_type": "pump",
            "status": "off",
            "latitude": 55.16941237711002,
            "longitude": -2.4152657705082987,
            "timestamp": dt.fromtimestamp(1641773400),
        },
        {
            "actuator_id": "test_actuator_1",
            "actuator_type": "pump",
            "status": "on",
            "longitude": -2.414782502162869,
            "latitude": 55.1680863785032,
            "timestamp": dt.fromtimestamp(1641773403),
        },
        {
            "actuator_id": "test_sprinkler_1",
            "actuator_type": "sprinkler",
            "status": "off",
            "longitude": -2.412569891209205,
            "latitude": 55.167951070033595,
            "timestamp": dt.fromtimestamp(1641773402),
        },
    ],
)

token = os.environ["INFLUXDB_TOKEN"]


def write_to_influxdb(payload):
    r = requests.post(
        f"{BASE_URL}/api/v2/write?org=WaterBeats&bucket=WaterBeats&precision=ns",
        data=payload,
        headers={
            "Authorization": f"Token {token}",
        },
    )
    if r.status_code != 204:
        print("Error writing to InfluxDB")
        print(r.text)


write_to_influxdb(payload)

actuator_data_payload = "\n".join(actuator_data_lines)
print(actuator_data_payload)
write_to_influxdb(actuator_data_payload)
