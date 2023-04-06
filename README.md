# WaterBeats

## Backend Service Database

We adopted a NoSQL timeseries database called InfluxDB to store the data.

Details [here](./TSDB/README.md).

## [Backend Data Service](./DataBackend/README.md)

## Front-end
The web front-end interface provides user with devices' visualisation, rules and alert management, and administrator tool.

Details [Front-end](./front-end/README.md).

## Authentication Gateway
Authentication Gateway acts as a proxy server between Front-end and the rest of back-end services in the Farmer PC. It responsible for authentication and authorisation. Then, it redirects the valid request to the target back-end service.

Details [Authentication Gateway](./AuthGateway/README.md).