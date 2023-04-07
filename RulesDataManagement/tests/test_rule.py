import json
import pytest
import sys
import uuid
from app import app


def test_get_rules():
    actuator_id_list = []
    n = 3
    for _ in range(n):
        payload = new_rule_payload()
        actuator_id_list.append(payload['actuator_id'])
        add_rule_response = add_rule(payload)

        assert add_rule_response.status_code == 201

    get_all_rules_response = get_all_rules()
    assert get_all_rules_response.status_code == 200

    all_rules_data = decode_response(get_all_rules_response)
    assert len(all_rules_data) >= n

    for actuator_id in actuator_id_list:
        get_rule_response = get_rule(actuator_id)
        assert get_rule_response.status_code == 200

        rule_data = decode_response(get_rule_response)

        assert rule_data["subject_sensor"] == payload["subject_sensor"]
        assert rule_data["sensor_reading"] == payload["sensor_reading"]
        assert rule_data["relation"] == payload["relation"]

        assert rule_data["actuator_id"] == actuator_id

        assert rule_data["actuator_type"] == payload["actuator_type"]
        assert rule_data["actuator_state"] == payload["actuator_state"]
        assert rule_data["intensity"] == payload["intensity"]
        assert rule_data["duration"] == payload["duration"]

def test_get_rule_missing_param():
    get_rule_response = get_rule()
    assert get_rule_response.status_code == 400

def test_add_rule():
    payload = new_rule_payload()

    add_rule_response = add_rule(payload)
    assert add_rule_response.status_code == 201

    add_rule_data = decode_response(add_rule_response)
    assert add_rule_data["actuator_id"] == payload["actuator_id"]

    get_rule_response = get_rule(payload["actuator_id"])
    assert get_rule_response.status_code == 200

    new_rule_data = decode_response(get_rule_response)

    assert new_rule_data["subject_sensor"] == payload["subject_sensor"]
    assert new_rule_data["sensor_reading"] == payload["sensor_reading"]
    assert new_rule_data["relation"] == payload["relation"]
    assert new_rule_data["actuator_id"] == payload['actuator_id']
    assert new_rule_data["actuator_type"] == payload["actuator_type"]
    assert new_rule_data["actuator_state"] == payload["actuator_state"]
    assert new_rule_data["intensity"] == payload["intensity"]
    assert new_rule_data["duration"] == payload["duration"]

def test_add_rule_missing_param():
    payload = new_rule_payload()

    for k in payload:
        missing_payload = payload.copy()
        missing_payload[k] = None

        add_rule_response = add_rule(missing_payload)
        assert add_rule_response.status_code == 400

def test_add_rule_already_exists():
    payload = new_rule_payload()

    first_add_rule_response = add_rule(payload)
    assert first_add_rule_response.status_code == 201

    second_add_rule_response = add_rule(payload)
    assert second_add_rule_response.status_code == 400

def test_update_rule():
    payload = new_rule_payload()

    add_rule_response = add_rule(payload)
    assert add_rule_response.status_code == 201

    add_rule_data = decode_response(add_rule_response)
    assert add_rule_data["actuator_id"] == payload["actuator_id"]

    updated_payload = update_rule_payload(payload["actuator_id"])

    update_rule_response = update_rule(updated_payload)
    assert update_rule_response.status_code == 200

    get_rule_response = get_rule(payload["actuator_id"])
    assert get_rule_response.status_code == 200

    rule_data = decode_response(get_rule_response)

    for data_key, data_value in updated_payload.items():
        assert rule_data[data_key] == data_value

def test_update_rule_missing_param():
    payload = update_rule_payload("00000")

    for k in payload:
        missing_payload = payload.copy()
        missing_payload[k] = None

        update_update_response = update_rule(missing_payload)
        assert update_update_response.status_code == 400

def test_update_rule_invalid_param():
    payload = update_rule_payload("00000")

    update_update_response = update_rule(payload)
    assert update_update_response.status_code == 400

def test_delete_rule():
    payload = new_rule_payload()

    add_rule_response = add_rule(payload)
    assert add_rule_response.status_code == 201

    added_actuator_id = decode_response(add_rule_response)["actuator_id"]
    assert added_actuator_id == payload["actuator_id"]

    delete_rule_response = delete_rule(payload["actuator_id"])
    assert delete_rule_response.status_code == 200

    delete_rule_data = decode_response(delete_rule_response)
    assert delete_rule_data["actuator_id"] == payload["actuator_id"]

    get_rule_response = get_rule(payload["actuator_id"])
    assert get_rule_response.status_code == 200

    rule_data = decode_response(get_rule_response)
    assert rule_data == None

def test_delete_missing_param():
    delete_rule_response = delete_rule()
    assert delete_rule_response.status_code == 400

def test_delete_invalid_param():
    delete_rule_response = delete_rule("00000")
    assert delete_rule_response.status_code == 400

# Helper Functions

def get_all_rules():
    return app.test_client().get("/rule/getAllRules")

def get_rule(actuator_id=""):
    if actuator_id:
        param = { "actuator_id": actuator_id }
    else:
        param = {}

    return app.test_client().get("/rule/getRuleByActuatorId", query_string=param)

def add_rule(payload):
    return app.test_client().post("/rule/addRule", query_string=payload)

def update_rule(payload):
    return app.test_client().put("/rule/updateRuleByActuatorId", query_string=payload)

def delete_rule(actuator_id=""):
    if actuator_id:
        param = { "actuator_id": actuator_id }
    else:
        param = {}

    return app.test_client().delete("/rule/deleteRuleByActuatorId", query_string=param)

def decode_response(response):
    return json.loads(response.data.decode("utf-8")).get("data")

def new_rule_payload():
    actuator_id = f"test_actuator_{uuid.uuid4().hex}"
    return {
        "subject_sensor": "test_sensor_0",
        "sensor_reading": 14,
        "relation": ">=",
        "actuator_id": actuator_id,
        "actuator_type": "sprinkler",
        "actuator_state": 1,
        "intensity": 80,
        "duration": 5
    }

def update_rule_payload(actuator_id):
    return {
        "subject_sensor": "test_sensor_1",
        "sensor_reading": 16,
        "relation": ">",
        "actuator_id": actuator_id,
        "actuator_state": 0,
        "intensity": 50,
        "duration": 3
    }
