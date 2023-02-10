import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

class DataManagement:
    
    def __init__(self, bucket: str, org: str, token: str, url: str):
        self.bucket = bucket
        self.org = org
        self.token = token
        self.url = url
        self.client = influxdb_client.InfluxDBClient(url=self.url, token=self.token, org=self.org)
        
    def write_data(self, data_point: influxdb_client.Point) -> str:
        """write data to the database

        Args:
            data_point (influxdb_client.Point): Data point

        Returns:
            str: status
        """
        try:
            with self.client.write_api(write_options=SYNCHRONOUS) as write_api:
                write_api.write(bucket=self.bucket, record=[data_point])
            return f"Data inserted"
        except Exception as e:
            return e
        
def insert_sensor_data(DM: DataManagement,sensor_id: str, sensor_type: str, data: float, unit: str, longitude: float, latitude: float, timestamp: int) -> str:
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
    data_point = influxdb_client.Point("sensor_data") \
        .tag("sensor_id", sensor_id) \
        .tag("sensor_type", sensor_type) \
        .field("data", data) \
        .field("unit", unit) \
        .field("longitude", longitude) \
        .field("latitude", latitude) \
        .time(timestamp)
    
    # * Write data to database
    response = DM.write_data(data_point)
    return response