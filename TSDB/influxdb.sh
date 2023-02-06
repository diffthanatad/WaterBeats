docker run \
    -e DOCKER_INFLUXDB_INIT_MODE=setup \
    -e DOCKER_INFLUXDB_INIT_USERNAME=WaterBeats \
    -e DOCKER_INFLUXDB_INIT_PASSWORD=WaterBeats \
    -e DOCKER_INFLUXDB_INIT_ORG=WaterBeats \
    -e DOCKER_INFLUXDB_INIT_BUCKET=WaterBeats \
    -p 8086:8086 \
    influxdb:2.6.1
