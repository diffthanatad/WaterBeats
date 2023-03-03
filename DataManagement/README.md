# Data Management
This is the end point server for receiving data from IoT base station

## Quick Start
- start influxDB on docker
- run api.py to run API server (If everything is already setup)
```shell
python api.py
```

## Required tools/software
- [Docker](https://www.docker.com/)
- [InfluxDB](https://www.influxdata.com/)

## Setup
1.  Install required packages
-  ```bash
    pip install -r requirements.txt
    ```
2. Start docker
3.  Install InfluxDB
4.  
### Install InfluxDB
- run this command via command line
```bash
docker run -e DOCKER_INFLUXDB_INIT_MODE=setup -e DOCKER_INFLUXDB_INIT_USERNAME=WaterBeats -e DOCKER_INFLUXDB_INIT_PASSWORD=WaterBeats -e DOCKER_INFLUXDB_INIT_ORG=WaterBeats -e DOCKER_INFLUXDB_INIT_BUCKET=WaterBeats -p 8086:8086 influxdb:2.6.1
```
---

## API routes
### Receiving sensor data route
```
POST localhost:5555/sensor_data
```
- example of JSON file
```json
{
  "sensor_id": "temperature_sensor_1",
  "sensor_type": "temperature",
  "data": 2.33,
  "unit": "C",
  "longitude": 2134,
  "latitude": 34135,
  "timestamp": 1675774426146000000
}
```

### Receiving actuator data route
```
POST localhost:5555/actuator_data
```
- example of JSON file
```json
{
  "actuator_id": "actuator_1",
  "actuator_type": "Sprinkler",
  "status": "activate",
  "longitude": 43145,
  "latitude": 43125,
  "timestamp": 1675774426146000000
}
```