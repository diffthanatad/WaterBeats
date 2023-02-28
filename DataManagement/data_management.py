import asyncio
import influxdb_client
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from influxdb_client.client.write_api import ASYNCHRONOUS

class DataManagement:
    @staticmethod
    async def insert_sensor_data(bucket: str, org: str, token: str, url: str,sensor_id: str, sensor_type: str, data: float, unit: str, longitude: float, latitude: float, timestamp: int) -> str:
        """insert data to database
        Args:
            sensor_id (int): Sensor ID
            sensor_type (str): Sensor type
            data (float): Data
            unit (str): Unit of the data
            longitude (float): Longitude of the sensor
            latitude (float): Latitude of the sensor
            timestamp (str): Timestamp of the data
        Raises:
            Exception: Error while inserting data to database
        Returns:
            str: Data inserted to database
        """
        # * Create data point
        data_point = influxdb_client.Point.measurement("sensor_data") \
            .tag("sensor_id", sensor_id) \
            .tag("sensor_type", sensor_type) \
            .field("data", data) \
            .field("unit", unit) \
            .field("longitude", longitude) \
            .field("latitude", latitude) \
            .time(timestamp)
        # * Write data to database
        async with InfluxDBClientAsync(url=url, token=token, org=org) as client:
            write_api = client.write_api()
            successfully = await write_api.write(bucket=bucket, record=[data_point])
            return f" > successfully: {successfully}"

    @staticmethod
    async def insert_actuator_data(bucket: str, org: str, token: str, url: str,actuator_id: str, actuator_type: str, status: str, longitude: float, latitude: float, timestamp: int) -> str:
        """insert data to database
        Args:
            actuator_id (int): Actuator ID
            actuator_type (str): Actuator type
            status (str): Status of the actuator
            longitude (float): Longitude of the actuator
            latitude (float): Latitude of the actuator
        Raises:
            Exception: Error while inserting data to database
        Returns:
            str: Data inserted to database
        """
        # * Create data point
        data_point = influxdb_client.Point("actuator_data") \
            .tag("actuator_id", actuator_id) \
            .tag("actuator_type", actuator_type) \
            .field("status", status) \
            .field("longitude", longitude) \
            .field("latitude", latitude) \
            .time(timestamp)
        # * Write data to database
        async with InfluxDBClientAsync(url=url, token=token, org=org) as client:
            write_api = client.write_api()
            successfully = await write_api.write(bucket=bucket, record=[data_point])
            return f" > successfully: {successfully}"
