# Time Series Database for WaterBeats

Timeseries database is a database that stores time series data. It is a collection of data points indexed in time order.

In the WaterBeats backend server, we use InfluxDB as the time series database.

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
