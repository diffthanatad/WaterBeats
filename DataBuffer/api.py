import json
from flask import Flask, make_response, request
import redis
from data_buffer import DataBuffer

app = Flask(__name__)


data_buffer = DataBuffer()


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
    key = f"{data['sensorId']}:{data['timestamp']}"
    fv_pairs = {
        "sensorType": data["sensorType"],
        "data": data["data"],
    }
    db.hset(key, fv_pairs)


def delete_sensor_data(db: DataBuffer, sensor_id, timestamp):
    key = f"{sensor_id}:{timestamp}"
    return db.delete(key)

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


def set_actuator_data(db: DataBuffer, data):
    key = f"{data['actuatorId']}:{data['timestamp']}"
    fv_pairs = {
        "sensorType": data["actuatorType"],
        "data": data["data"],
    }
    db.hset(key, fv_pairs)


def delete_actuator_data(db: DataBuffer, actuator_id, timestamp):
    key = f"{actuator_id}:{timestamp}"
    return db.delete(key)

@app.errorhandler(redis.exceptions.ConnectionError)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    print(e)
    response = make_response()
    response.data = json.dumps(
        {
            "erroNo": 4,
            "message": "Redis connection error",
            "data": None,
        }
    )
    response.status_code = 500
    response.content_type = "application/json"
    return response


@app.route("/sensor", methods=["GET", "POST", "DELETE"])
def sensor_api():
    if request.method == "GET":
        sensor_id = request.args.get("sensorId")
        timestamp = request.args.get("timestamp")
        data = get_sensor_data(data_buffer, sensor_id, timestamp)
        if data is None:
            return ("", 204)
        resp_body = {"erroNo": 0, "message": "OK", "data": data}
        return (resp_body, 200)
    elif request.method == "POST":
        data = request.json
        set_sensor_data(data_buffer, data)
        return ("", 201)
    elif request.method == "DELETE":
        sensor_id = request.args.get("sensorId")
        timestamp = request.args.get("timestamp")
        nums_del = delete_sensor_data(data_buffer, sensor_id, timestamp)
        if nums_del == 0:
            return ("", 204)
        return ("", 202)

@app.route("/instruction", methods=["GET", "POST", "DELETE"])
def actuator_api():
    if request.method == "GET":
        actuator_id = request.args.get("actuatorId")
        timestamp = request.args.get("timestamp")
        data = get_instruction_data(data_buffer, actuator_id, timestamp)
        if data is None:
            return ("", 204)
        resp_body = {"erroNo": 0, "message": "OK", "data": data}
        return (resp_body, 200)
    elif request.method == "POST":
        data = request.json
        set_actuator_data(data_buffer, data)
        return ("", 201)
    elif request.method == "DELETE":
        actuator_id = request.args.get("actuatorId")
        timestamp = request.args.get("timestamp")
        nums_del = delete_actuator_data(data_buffer, actuator_id, timestamp)
        if nums_del == 0:
            return ("", 204)
        return ("", 202)


if __name__ == "__main__":
    app.run(host="localhost", port=23333, debug=True)
