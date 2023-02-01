from service import set_sensor_data, pop_sensor_data
from data_buffer import DataBuffer


def test_set_and_pop():
    db = DataBuffer()
    set_sensor_data(
        db, {"sensorId": "a", "timestamp": 1, "sensorType": "b", "data": "c"}
    )
    ret = pop_sensor_data(db, "a")
    print(ret)


def test_sensor_data_list():
    db = DataBuffer()
    db.hset_sorted(
        "sensor1",
        {"sensorType": "1", "data": 0.1},
        1675102350,
        "ts",
        "sensor1",
        "sensors_set",
    )
    db.hset_sorted(
        "sensor2",
        {"sensorType": "1", "data": 42},
        1675102370,
        "ts",
        "sensor2",
        "sensors_set",
    )
    data = db.get_all_by_value_range("sensors_set", 0, 1675102370)
    assert len(data) == 2
    data = db.get_all_by_value_range("sensors_set", 0, 1675102360)
    assert len(data) == 1
    assert data[0][b'data'] == b'0.1'


def test_sensor_data_delete_by_timestamp():
    db = DataBuffer()
    db.hset_sorted(
        "sensor1:1",
        {"sensorType": "1", "data": 0.1},
        1675102350,
        "sensor1_ts",
        "sensor1:1",
        "sensors_set",
    )
    db.hset_sorted(
        "sensor2:1",
        {"sensorType": "1", "data": 42},
        1675102370,
        "sensor1_ts",
        "sensor2:1",
        "sensors_set",
    )
    db.hset_sorted(
        "sensor2:2",
        {"sensorType": "1", "data": 233},
        1675102390,
        "sensor2_ts",
        "sensor2:2",
        "sensors_set",
    )
    db.delete_all_by_value_range("sensors_set", 0, 1675102380)
    data = db.get_all_by_value_range("sensors_set", 0, 1675102400)
    assert len(data) == 1
    print(data)
    assert data[0][b'data'] == b'233'