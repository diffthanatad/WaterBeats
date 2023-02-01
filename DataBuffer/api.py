import json
from flask import Flask, make_response, request
import redis
from service import (
    delete_actuator_data,
    delete_sensor_data,
    get_instruction_data,
    get_sensor_data,
    pop_top_instruction,
    set_instruction,
    set_sensor_data,
)
import service
from data_buffer import DataBuffer

app = Flask(__name__)


data_buffer = DataBuffer()



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

@app.route("/sensor/history", methods=["GET", "DELETE"])
def sensor_list_api():
    if request.method == "GET":
        timestamp = request.args.get("timestamp")
        data = service.get_history_sensor_data_by_timestamp(data_buffer, timestamp)
        if data is None:
            return ("", 204)
        resp_body = {"erroNo": 0, "message": "OK", "data": data}
        return (resp_body, 200)
    elif request.method == "DELETE":
        timestamp = request.args.get("timestamp")
        service.delete_history_sensor_data_by_timestamp(data_buffer, timestamp)
        return ("", 200)
    

#### Instruction API ####

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
        set_instruction(data_buffer, data)
        return ("", 201)
    elif request.method == "DELETE":
        actuator_id = request.args.get("actuatorId")
        timestamp = request.args.get("timestamp")
        nums_del = delete_actuator_data(data_buffer, actuator_id, timestamp)
        if nums_del == 0:
            return ("", 204)
        return ("", 202)


@app.route("/instruction/pop", methods=["GET"])
def instruction_pop():
    actuator_id = request.args.get("actuatorId")
    data = pop_top_instruction(data_buffer, actuator_id)
    if data is None:
        return ("", 204)
    print('got data: ', data)
    resp_body = {"erroNo": 0, "message": "OK", "data": data}
    return (resp_body, 200)


if __name__ == "__main__":
    app.run(host="localhost", port=23333, debug=True)
