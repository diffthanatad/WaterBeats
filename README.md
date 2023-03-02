# Base Station

This branch contains the full base station functionality.

## Features

- stream processing using Faust
- sensor and actuator event management
- sensor and actuator interfaces for Faust
- sensor and actuator firmware for ESP32
- local database and cloud database connections

## Prerequisites
### Download Kafka
Download the latest stable Apache Kafka (3.4.0) binary for Scala 2.13 from https://kafka.apache.org/downloads.

Extract to the root directory (e.g., C:\ on Windows) and rename the directory to kafka.

### Set up a Python environment
Create a python virtual environment
```
python -m venv bs_env
```

Activate the environment appropriately in `bs_env/Scripts/`

Install packages from requirements.txt
```
pip install -r requirements.txt
```

## Quick start

### Start zookeeper and kafka, then start a Faust worker
On Windows: `start_kafka.bat` then `start_faust.bat`

On MacOS: `start_kafka.sh` then `start_faust.sh`

### Sending messages manually
Each sensor readings channel is reponsible for one sensor type and has a corresponding agent to process these messages.  
You can send a message to a channel manually (e.g., to @humidity_stream).

On Windows: `faust -A base_station send @humidity_stream "{"""sensor_id""": """test_sensor1""", """reading""": """15"""}"`

On MacOS: `faust -A base_station send @humidity_stream '{"sensor_id": "test_sensor1", "reading": "15"}'`
