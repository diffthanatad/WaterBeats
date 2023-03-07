# Base Station

The full base station functionality for our scalable IoT smart farming solution.  
It works standalone via command-line, but is even better with the Main Hub to aggregate, display, and control devices, data and rules!  
Just connect your sensors and actuators, then add smart rules to automatically manage your devices. That's it!

Runs on a personal computer, dedicated hardware, or even a Raspberry Pi.

## Features

- highly scalable streaming of IoT sensor data
- connect any IoT sensor or actuator using our interface for handling JSON messages
- process sensor data using lambda architecture with stream and batch processing routes
- store sensor data locally, forward it to a data hub, or upload directly to cloud storage
- automatically control actuators with rules containing tasks and conditions
- receive and apply rule and tasks remotely
- works online or offline for remote farming conditions
- data persistence and recovery built-in for power loss and poor connection scenarios

## Prerequisites
### Download Kafka
Download the latest stable Apache Kafka (3.4.0) binary for Scala 2.13 from https://kafka.apache.org/downloads.

On Windows, extract to the root directory (e.g., C:\) and rename the directory to kafka.  
On MacOS, extract to the user home directory (e.g., /Users/name/) and rename the directory to kafka.


### Set up a Python environment
Create a python virtual environment
```
python -m venv bs_env
```

Activate the environment appropriately in `./bs_env/Scripts/`

Install packages from requirements.txt
```
pip install -r requirements.txt
```

## Quick start
### Add a record of sensors and actuators
Supply the relevant information for your sensors and actuators in `./base_station/local_data/`

Here are some example values for `sensors.csv`
| sensor_id | sensor_type | reading_unit | latitude | longitude |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| 30:AE:A4:14:C2:90 | humidity sensor | Percent | 51.509865 | -0.118092 |
| F4:12:FA:83:00:F0 | temperature sensor | Celsius | 51.508610 | -0.163611 |

All fields including sensor_id can be changed freely. This example uses MAC addresses as sensor_ids.  
Longitude and latitude can be added to provide a map view of devices on the Main Hub web interface.

### Start zookeeper and kafka, then start a Faust worker
On Windows: `start_kafka.bat` then `start_faust.bat`

On MacOS: `start_kafka.sh` then `start_faust.sh`

### Connect your sensors and actuators
Run `Faust/interfaces/sensor_interface.py` to start a local server and start communicating with IoT devices.  
Post sensor data in standard JSON format containing only sensor_id and a reading.  
Working examples are provided in `physical_devices/` for two ESP32 variants using the dht11 temperature and humidity sensor.

## Testing
Change directory to `./base_station/`

Run `python -m pytest`

## User Guide
### Sending messages to channels
Kafka channels are used to separate each message type: sensor, actuator, task, and rule messages  
Use our message interface at `base_station/interfaces/producer.py` to send messages to these channels directly.

```
producer.send_rule_message(rule_message = RuleMessage(task_message, condition_message), flush = True)
```

Alternatively, you can send a message to a channel through command-line.

On Windows: `faust -A base_station send @sensor_stream "{"""sensor_id""": """test_sensor1""", """reading""": """15"""}"`

On MacOS: `faust -A base_station send @sensor_stream '{"sensor_id": "test_sensor1", "reading": "15"}'`
