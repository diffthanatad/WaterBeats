from data_buffer import DataBuffer

def parse_sensor_data_from_bytes(data: dict) -> dict:
    return {
        "sensorId": str(data[b'sensorId'], encoding='utf8'),
        "timestamp": int(data[b'timestamp']),
        "sensorType": str(data[b'sensorType'], encoding='utf8'),
        "data": float(data[b'data']),
    }

def get_sensor_data(data_buffer: DataBuffer, sensor_id, timestamp):
    key = f"{sensor_id}:{timestamp}"
    fvs = data_buffer.hgetall(key)
    if not fvs:
        return None
    return {
        "sensorId": sensor_id,
        "timestamp": timestamp,
        "sensorType": str(fvs[b"sensorType"], encoding="utf-8"),
        "data": float(fvs[b"data"]),
    }


def set_sensor_data(db: DataBuffer, data):
    id = data["sensorId"]
    ts = data["timestamp"]
    key = f"{id}:{ts}"
    fv_pairs = {
        "sensorType": data["sensorType"],
        "data": data["data"],
        "sensorId": id,
        "timestamp": ts,
    }
    db.hset_sorted(key, fv_pairs, ts, id, key, set_key="sensors_set")

def get_history_sensor_data_by_timestamp(db: DataBuffer, timestamp: int):
    ret= db.get_all_by_value_range("sensors_set", 0, timestamp)
    ret = list(map(parse_sensor_data_from_bytes, ret))
    return ret

def delete_history_sensor_data_by_timestamp(db: DataBuffer, timestamp: int):
    return db.delete_all_by_value_range("sensors_set", 0, timestamp)

def delete_sensor_data(db: DataBuffer, sensor_id, timestamp):
    key = f"{sensor_id}:{timestamp}"
    return db.delete(key)



def pop_sensor_data(db: DataBuffer, sensor_id):
    fvs = db.pop_sorted(sensor_id, ["sensorType", "data"])
    return fvs

def get_instruction_data(data_buffer: DataBuffer, actuator_id, timestamp):
    key = f"{actuator_id}:{timestamp}"
    fvs = data_buffer.hgetall(key)
    if not fvs:
        return None
    return {
        "actuatorId": actuator_id,
        "timestamp": timestamp,
        "actuatorType": str(fvs[b"actuatorType"], encoding="utf-8"),
        "data": float(fvs[b"data"]),
    }


def pop_top_instruction(data_buffer: DataBuffer, actuator_id):
    popped = data_buffer.pop_sorted(actuator_id, ["timestamp", "actuatorType", "data"])
    if not popped:
        return None
    member, fvs = popped
    return {
        "actuatorId": actuator_id,
        "timestamp": str(member).split(':')[1],
        "actuatorType": str(fvs[1]),
        "data": str(fvs[2], encoding="utf-8"),
    }

def set_instruction(db: DataBuffer, data):
    id = data["actuatorId"]
    ts = data["timestamp"]
    key = f"{id}:{ts}"
    fv_pairs = {
        "sensorType": data["actuatorType"],
        "data": data["data"],
    }
    db.hset_sorted(key, fv_pairs, ts, id, key)


def delete_actuator_data(db: DataBuffer, actuator_id, timestamp):
    key = f"{actuator_id}:{timestamp}"
    return db.delete(key)