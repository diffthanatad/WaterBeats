# Data Backend

This is the data service for the WaterBeats frontend.
It provides access to environmental sensor and actuator data. The API is designed with a series of HTTP endpoints that handle querying data from the sensors and actuators, as well as debugging purposes.

## Quick Start

Create an InfluxDB token [as described](../TSDB/README.md#create-api-tokens-for-other-services).

```sh
export INFLUXDB_TOKEN=... # your token
export INFLUXDB_HOST=localhost:8086 # OPTIONAL, your InfluxDB URL
export INFLUXDB_ORG=WaterBeats # OPTIONAL, your InfluxDB organization name
export WB_ADDRESS=localhost:8080 # OPTIONAL, the address to bind to
cargo run
```

## Core Dependencies

This data service is created with [tide](https://github.com/http-rs/tide).

The InfluxDB data access layer is implemented with [influxdb2](https://github.com/aprimadi/influxdb2).

## Function Overview

Key functions include:

- Retrieving latest records from all sensors
- Retrieving latest record by sensor ID
- Retrieving sensor data by ID and a time range
- Retrieving latest data from all devices
- Retrieving latest actuator data by type

API Endpoints:

- /sensor/allLatest: GET request to retrieve the latest records from all sensors.
- /sensor/getLatestById: GET request to retrieve the latest record for a specific sensor, based on the provided sensor ID.
- /sensor/record: GET request to retrieve sensor data for a specific sensor by its ID and a specified time range.
- /device/latest: GET request to retrieve the latest data from all devices.
- /actuator/latestByType: GET request to retrieve the latest data for actuators of a specific type.

Middleware:

- CORS: Configure Cross-Origin Resource Sharing (CORS) to allow requests from any origin and specific HTTP methods.
- Logging: Add logging middleware for request and response logging.

API Response Format:

- `ApiResponse` struct: Contains error, message, and data fields to represent the API response.
Data Models:
