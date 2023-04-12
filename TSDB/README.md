# Time Series Database for WaterBeats

Timeseries database is a database that stores time series data. It is a collection of data points indexed in time order.

In the WaterBeats backend server, we use InfluxDB as the time series database. InfluxDB is a time-series database used for handling high-write and query loads, particularly well-suited for IoT and monitoring use cases.

## Setup

### Starting an InfluxDB instance with docker

```sh
./influxdb.sh
```

This scripts starts an InfluxDB instance with default username(`WaterBeats`), password(`WaterBeats`), and bucket(`WaterBeats`) initialized.

### Create API tokens for other services

```sh
python create_token.py
```

This script creates an API token for other backend services to access the `WaterBeats` bucket with read/write permissions. The script uses the default username, password and bucket name as in the previous setup step. The token is shown in the last line of the output, if successful.

There is no limit on the number of tokens that can be created. Therefore you can run `INFLUXDB_TOKEN=$(python create_token.py | tail -n 1) ./command-to-your-service` every time to authenticate your service to the InfluxDB instance.

## Initialize InfluxDB data

```sh
INFLUXDB_TOKEN=$(python create_token.py | tail -n 1) python init_data.py
```

## Database Demo Data Generation Script

[The code](init_data.py) is a Python script that generates sample environmental sensor and actuator data, and stores the data into an InfluxDB database.

The script generates data for five sensors and three actuators. The SensorDataGenerator class is responsible for simulating sensor data, while the actuator data is hard-coded. The sensors measure temperature, soil moisture, water level, and water pollution, and the actuators control pumps and sprinklers.

Sensor Data:
Each sensor is represented by a SensorDataGenerator object, which takes four arguments: sensor_id, sensor_type, unit, and coordinates (as a tuple). The generator uses a sin function to create a semi-random fluctuation in the sensor data, with added noise to simulate realistic readings. The sensor data includes a status field that can be set to "on," "off," or "error."

Actuator Data:
The actuator data consists of hard-coded dictionaries with the following fields: actuator_id, actuator_type, status, longitude, latitude, and timestamp.

InfluxDB Integration:
The InfluxDB token and base URL are provided as environment variables. The script uses the "requests" library to send POST requests to the InfluxDB API, writing sensor and actuator data to the database.

Data Format:
Sensor and actuator data are formatted as InfluxDB line protocol strings. The line protocol is a text-based format that provides a compact and efficient way to represent time-series data. For example, the sensor data line protocol format is:

```
sensor_data,sensor_id=<sensor_id>,sensor_type=<sensor_type> unit="<unit>",longitude=<longitude>,latitude=<latitude>,data=<data>,status="<status>" <timestamp>
```

The actuator data line protocol format is:

```
actuator_data,actuator_id=<actuator_id>,actuator_type=<actuator_type> status="<status>",longitude=<longitude>,latitude=<latitude> <timestamp>
```

These line protocol strings are then combined into a payload and sent to the InfluxDB API.

## Database Schema

Schema of the Database:

The database schema is designed to store time-series data for environmental sensors and actuators. It consists of two separate measurements: sensor_data and actuator_data.

sensor_data measurement:

Tags:
sensor_id (string): Unique identifier for each sensor.

sensor_type (string): The type of sensor, e.g., temperature, soil moisture, water level, or water pollution.

Fields:

unit (string): The unit of the sensor data, e.g., degrees Fahrenheit (F) or Celsius (C), percentage (%), millimeters (mm), or parts per million (ppm).

longitude (float): The longitude of the sensor's location.

latitude (float): The latitude of the sensor's location.

data (float): The sensor's reading at the given timestamp.

status (string): The status of the sensor, which can be "on," "off," or "error."

Timestamp: Unix timestamp (nanoseconds precision) when the sensor data was recorded.

actuator_data measurement:

Tags:

actuator_id (string): Unique identifier for each actuator.

actuator_type (string): The type of actuator, e.g., pump or sprinkler.

Fields:

status (string): The status of the actuator, which can be "on" or "off."

longitude (float): The longitude of the actuator's location.

latitude (float): The latitude of the actuator's location.

Timestamp: Unix timestamp (nanoseconds precision) when the actuator data was recorded.
