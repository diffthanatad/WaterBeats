from data_management import DataManagement, insert_sensor_data
from create_token import find_waterbeats_buckets, create_token_for_bucket
import pytest

WB_bucket = find_waterbeats_buckets()
WB_token = create_token_for_bucket(WB_bucket["id"],WB_bucket["orgID"])
WB_datamanagement = DataManagement(WB_bucket['name'], WB_bucket["orgID"], WB_token, "http://localhost:8086")



@pytest.mark.asyncio
async def test_insert_sensor_data():
    sensor_id = "test_sensor"
    sensor_type = "test_type"
    sensor_data = 50
    unit = "test_unit"
    longitude = 0
    latitude = 0
    timestamp = "2021-02-22T15:00:00Z"
    response = await insert_sensor_data(WB_datamanagement, sensor_id, sensor_type, sensor_data, unit, longitude, latitude, timestamp)
    assert response == "Data inserted"