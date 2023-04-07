import json
import pytest
import sys
import uuid
from app import app


def test_get_alerts():
    sensor_id_list = []
    n = 3
    for _ in range(n):
        payload = new_alert_payload()
        sensor_id_list.append(payload["sensor_id"])
        add_alert_response = add_alert(payload)

        assert add_alert_response.status_code == 201

    get_all_alerts_response = get_all_alerts()
    assert get_all_alerts_response.status_code == 200

    all_alerts_data = decode_response(get_all_alerts_response)
    assert len(all_alerts_data) >= n

    for sensor_id in sensor_id_list:
        get_alert_response = get_alert(sensor_id)
        assert get_alert_response.status_code == 200

        alert_data = decode_response(get_alert_response)

        assert alert_data["sensor_id"] == sensor_id
        assert alert_data["sensor_type"] == payload["sensor_type"]
        assert alert_data["threshold"] == payload["threshold"]
        assert alert_data["relation"] == payload["relation"]

def test_get_alert_missing_param():
    get_alert_response = get_alert()
    assert get_alert_response.status_code == 400

def test_add_alert():
    payload = new_alert_payload()

    add_alert_response = add_alert(payload)
    assert add_alert_response.status_code == 201

    add_alert_data = decode_response(add_alert_response)
    assert add_alert_data["sensor_id"] == payload["sensor_id"]

    get_alert_response = get_alert(payload["sensor_id"])
    assert get_alert_response.status_code == 200

    new_alert_data = decode_response(get_alert_response)

    assert new_alert_data["sensor_id"] == payload["sensor_id"]
    assert new_alert_data["sensor_type"] == payload["sensor_type"]
    assert new_alert_data["threshold"] == payload["threshold"]
    assert new_alert_data["relation"] == payload["relation"]

def test_add_alert_missing_param():
    payload = new_alert_payload()

    for k in payload:
        missing_payload = payload.copy()
        missing_payload[k] = None

        add_alert_response = add_alert(missing_payload)
        assert add_alert_response.status_code == 400

def test_add_alert_already_exists():
    payload = new_alert_payload()

    add_alert_response = add_alert(payload)
    assert add_alert_response.status_code == 201

    add_alert_response = add_alert(payload)
    assert add_alert_response.status_code == 400

def test_update_alert():
    payload = new_alert_payload()

    add_alert_response = add_alert(payload)
    assert add_alert_response.status_code == 201

    add_alert_data = decode_response(add_alert_response)
    assert add_alert_data["sensor_id"] == payload["sensor_id"]

    updated_payload = update_alert_payload(payload["sensor_id"])

    update_alert_response = update_alert(updated_payload)
    assert update_alert_response.status_code == 200

    updated_alert_data = decode_response(update_alert_response)
    assert updated_alert_data["sensor_id"] == payload["sensor_id"]

    get_alert_response = get_alert(payload["sensor_id"])
    assert get_alert_response.status_code == 200

    alert_data = decode_response(get_alert_response)

    assert alert_data["threshold"] == updated_payload["threshold"]
    assert alert_data["relation"] == updated_payload["relation"]

def test_update_alert_missing_param():
    payload = update_alert_payload(uuid.uuid4().hex)

    for k in payload:
        missing_payload = payload.copy()
        missing_payload[k] = None

        update_update_response = update_alert(missing_payload)
        assert update_update_response.status_code == 400

def test_delete_alert():
    payload = new_alert_payload()

    add_alert_response = add_alert(payload)
    assert add_alert_response.status_code == 201

    add_alert_data = decode_response(add_alert_response)
    assert add_alert_data["sensor_id"] == payload["sensor_id"]

    delete_alert_response = delete_alert(payload["sensor_id"])
    assert delete_alert_response.status_code == 200

    deleted_alert_data = decode_response(delete_alert_response)
    assert deleted_alert_data["sensor_id"] == payload["sensor_id"]

    get_alert_response = get_alert(payload["sensor_id"])
    assert get_alert_response.status_code == 200

    alert_data = decode_response(get_alert_response)
    assert alert_data == None

def test_delete_alert_missing_param():
    delete_alert_response = delete_alert()
    assert delete_alert_response.status_code == 400


# Helper Functions

def get_all_alerts():
    return app.test_client().get("/alert/getAllAlerts")

def get_alert(sensor_id=""):
    if sensor_id:
        param = { "sensor_id": sensor_id }
    else:
        param = {}

    return app.test_client().get("/alert/getAlertBySensorId", query_string=param)

def add_alert(payload):
    return app.test_client().post("/alert/addAlert", query_string=payload)

def update_alert(payload):
    return app.test_client().put("/alert/updateAlertBySensorId", query_string=payload)

def delete_alert(sensor_id=""):
    if sensor_id:
        param = { "sensor_id": sensor_id }
    else:
        param = {}
    return app.test_client().delete("alert/deleteAlertBySensorId", query_string=param)

def decode_response(response):
   return json.loads(response.data.decode("utf-8")).get("data")

def new_alert_payload():
    sensor_id = f"sensor_{uuid.uuid4().hex}"
    return {
        "sensor_id": sensor_id,
        "sensor_type": "temperature",
        "threshold": 12,
        "relation": ">="
    }

def update_alert_payload(sensor_id):
    return {
        "sensor_id": sensor_id,
        "sensor_type": "temperature",
        "threshold": 16,
        "relation": ">"
    }
