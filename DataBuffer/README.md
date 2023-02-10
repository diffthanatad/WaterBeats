# DataBuffer

## Quick Start

```sh
docker run -p 6379:6379 --rm redis # start a redis instance
python -m pip install DataBuffer # install the dependencies
python api.py # start the server
```

## Data Models

### Sensor Data Record

1. hashed key-value mapping: "{sensorId}:{timestamp}" -> {sensorType: "temperature", data: 23.4, timestamp: 1675084350, ...}
2. ZLIST
   - list key: sensorId
   - member: "{sensorType}:{timestamp}"
   - score: timestamp
