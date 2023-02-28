from pathlib import Path
import csv
from enum import Enum

class SensorType(Enum):
    HUMIDITY_SENSOR = 'humidity sensor'
    TEMPERATURE_SENSOR = 'temperature sensor'
    SOIL_MOISTURE_SENSOR = 'soil moisture sensor'

class ActuatorType(Enum):
    SPRINKLER = 'sprinkler'
    PUMP = 'pump'
    MOTOR = 'motor'

class Device:
    def __init__(self, device_id: str, device_type: str, latitude: float, longitude: float):
        self.device_id = device_id
        self.device_type = device_type
        self.latitude = latitude
        self.longitude = longitude

class Sensor(Device):
    def __init__(self, sensor_id: str, sensor_type: SensorType, reading_unit: str, longitude: float, latitude: float):
        super().__init__(sensor_id, sensor_type, longitude, latitude)
        self.reading_unit = reading_unit

class Actuator(Device):
    def __init__(self, actuator_id: str, actuator_type: ActuatorType, longitude:float, latitude: float):
        super().__init__(actuator_id, actuator_type, longitude, latitude)
        self.state: bool = False

script_location = Path(__file__).absolute().parent
file_location = script_location / 'local_data/sensors.csv'

sensors = {}

try:
    with open(file_location, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader, None) # sensor_id,sensor_type,reading_unit,latitude,longitude
        for row in reader:
            sensors[row[0]] = Sensor(*row)

except Exception as e:
    print(e)

#print(sensors['30:AE:A4:14:C2:90'].device_id)

print(sensors)

def getSensorData(sensor_id):
    return sensors[sensor_id]








class Condition:
    time: str = None
    recurring: bool = False
    subject: Sensor = None
    reading: float = None
    relation: str = None

class Instruction:
    """Instructions to an actuator.

    Attributes:
        target      The actuator target to control
        state       The intended on/off state of the instruction to the target
        intensity   E.g., rotational speed of motor, pressure of sprinkler. Between 0 and 1.
        duration    Optional duration until reversion to previous state. -1 for indefinite duration.
    """
    target: Actuator
    state: str
    intensity: float
    duration: int = -1
    condition: Condition = None