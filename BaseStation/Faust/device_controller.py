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
    def __init__(self, sensor_id: str, sensor_type: SensorType, reading_unit: str, latitude: float, longitude: float):
        super().__init__(sensor_id, sensor_type, latitude, longitude)
        self.reading_unit = reading_unit

class Actuator(Device):
    def __init__(self, actuator_id: str, actuator_type: ActuatorType, latitude: float, longitude: float):
        super().__init__(actuator_id, actuator_type, latitude, longitude)



sensors = {}
actuators = {}

script_location = Path(__file__).absolute().parent

try:
    file_location = script_location / 'local_data/sensors.csv'

    with open(file_location, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader, None) # sensor_id,sensor_type,reading_unit,latitude,longitude
        for row in reader:
            sensors[row[0]] = Sensor(*row)

    file_location = script_location / 'local_data/actuators.csv'
    
    with open(file_location, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader, None) # actuator_id,actuator_type,latitude,longitude
        for row in reader:
            actuators[row[0]] = Actuator(*row)

except Exception as e:
    print(e)

def getSensorData(sensor_id):
    return sensors.get(sensor_id, None)

def getActuatorData(actuator_id):
    return actuators.get(actuator_id, None)