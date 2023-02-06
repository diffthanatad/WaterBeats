# Data Backend

This is the data service for the WaterBeats frontend.

## Quick Start

Create an InfluxDB token [as described](../TSDB/README.md#create-api-tokens-for-other-services).

```sh
export INFLUXDB_TOKEN=... # your token
export INFLUXDB_HOST=localhost:8086 # OPTIONAL, your InfluxDB URL
export INFLUXDB_ORG=WaterBeats # OPTIONAL, your InfluxDB organization name
export WB_ADDRESS=localhost:8080 # OPTIONAL, the address to bind to
cargo run
```

## Development

This data service is created with [tide](https://github.com/http-rs/tide).

The InfluxDB data access layer is implemented with [influxdb2](https://github.com/aprimadi/influxdb2).
