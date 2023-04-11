import copy
import json
import pytest
import sys
import uuid
from influxdb import InfluxDB


def test_get_alert():
    influxdb = InfluxDB()
    sensor_id = "sensor_" + uuid.uuid4().hex
    alert_id = influxdb.create_alert(sensor_id, "temperature", 18, ">")

    assert influxdb.get_alert("alert_" + sensor_id)["id"] == alert_id

def test_get_alert_none():
    influxdb = InfluxDB()
    sensor_id = "sensor_" + uuid.uuid4().hex

    assert influxdb.get_alert("alert_" + sensor_id) == None

def test_create_alert():
    influxdb = InfluxDB()
    sensor_id = "sensor_" + uuid.uuid4().hex
    threshold = 18
    sensor_type = "temperature"
    relation = ">"

    alert_id = influxdb.create_alert(sensor_id, sensor_type, threshold, relation)
    alert = influxdb.get_alert("alert_" + sensor_id)

    assert alert["id"] == alert_id
    assert (sensor_id in alert["query"]["text"]) == True
    assert (sensor_type in alert["query"]["text"]) == True
    assert alert["thresholds"][0]["value"] == threshold
    assert alert["thresholds"][0]["type"] == "greater"

    for tag in alert["query"]["builderConfig"]["tags"]:
        if tag["key"] == "sensor_id":
            assert tag["values"] == [sensor_id]
        if tag["key"] == "sensor_type":
            assert tag["values"] == [sensor_type]

def test_update_alert():
    influxdb = InfluxDB()
    sensor_id = "sensor_" + uuid.uuid4().hex
    initial_threshold = 18

    alert_id = influxdb.create_alert(sensor_id, "temperature", initial_threshold, ">")
    added_alert = influxdb.get_alert("alert_" + sensor_id)

    assert added_alert["id"] == alert_id
    assert added_alert["thresholds"][0]["value"] == initial_threshold

    new_threshold = 30
    assert influxdb.update_alert(sensor_id, "temperature", new_threshold, ">") == True

    updated_alert = influxdb.get_alert("alert_" + sensor_id)
    assert updated_alert["id"] == alert_id
    assert updated_alert["thresholds"][0]["value"] == new_threshold

def test_update_alert_false():
    influxdb = InfluxDB()
    sensor_id = "sensor_" + uuid.uuid4().hex

    assert influxdb.update_alert(sensor_id, "temperature", 18, ">") == False

def test_delete_alert():
    influxdb = InfluxDB()
    sensor_id = "sensor_" + uuid.uuid4().hex
    alert_id = influxdb.create_alert(sensor_id, "temperature", 18, ">")

    assert influxdb.get_alert("alert_" + sensor_id)["id"] == alert_id
    assert influxdb.delete_alert(sensor_id) == True
    assert influxdb.get_alert("alert_" + sensor_id) == None

def test_delete_alert_false():
    influxdb = InfluxDB()
    sensor_id = "sensor_" + uuid.uuid4().hex
    is_deleted = influxdb.delete_alert(sensor_id)

    assert is_deleted == False

def test_get_notification_endpoint():
    influxdb = InfluxDB()
    payload = copy.deepcopy(influxdb.endpoint_payload)
    payload["name"] = "twilio_endpoint_" + uuid.uuid4().hex

    add_endpoint_id = influxdb.add_notification_endpoint(payload)
    assert add_endpoint_id != False

    get_endpoint_id = influxdb.get_notification_endpoint(payload["name"])
    assert add_endpoint_id == get_endpoint_id

def test_get_notification_endpoint_none():
    influxdb = InfluxDB()
    endpoint_name = "twilio_endpoint_" + uuid.uuid4().hex

    assert influxdb.get_notification_endpoint(endpoint_name) == None

def test_add_notification_endpoint():
    influxdb = InfluxDB()
    payload = copy.deepcopy(influxdb.endpoint_payload)
    payload["name"] = "twilio_endpoint_" + uuid.uuid4().hex
    endpoint_id = influxdb.add_notification_endpoint(payload)

    assert endpoint_id != False

def test_get_notification_rule_none():
    influxdb = InfluxDB()
    rule_name = "alert_rule_" + uuid.uuid4().hex

    assert influxdb.get_notification_rule(rule_name) == None

def test_create_notification_rule():
    influxdb = InfluxDB()

    e_payload = copy.deepcopy(influxdb.endpoint_payload)
    e_payload["name"] = "twilio_endpoint_" + uuid.uuid4().hex
    endpoint_id = influxdb.add_notification_endpoint(e_payload)

    r_payload = copy.deepcopy(influxdb.rule_payload)
    r_payload["name"] = "alert_rule_" + uuid.uuid4().hex
    r_payload["endpointID"] = endpoint_id

    created_rule_id = influxdb.create_notification_rule(r_payload)
    assert created_rule_id != False

    get_rule_id = influxdb.get_notification_rule(r_payload["name"])
    assert get_rule_id == created_rule_id

def test_set_alert_payload():
    influxdb = InfluxDB()
    alert_name = "alert_" + uuid.uuid4().hex
    sensor_id = "sensor_" + uuid.uuid4().hex
    sensor_type = "temperature"
    threshold = 18
    relation = ">"
    alert_id = "id_" + uuid.uuid4().hex

    payload =  influxdb.set_alert_payload(alert_name, sensor_id, sensor_type, threshold, relation, alert_id)

    assert(payload["name"] == alert_name)
    assert(payload["checkID"] == alert_id)

    assert (sensor_id in payload["query"]["text"]) == True
    assert (sensor_type in payload["query"]["text"]) == True

    assert (payload["thresholds"][0]["value"] == threshold)
    assert (payload["thresholds"][0]["type"] == "greater")

    relation = ">="
    payload =  influxdb.set_alert_payload(alert_name, sensor_id, sensor_type, threshold, relation, alert_id)

    assert (payload["thresholds"][0]["value"] == (threshold - 1))
    assert (payload["thresholds"][0]["type"] == "greater")

    relation = "<"
    payload =  influxdb.set_alert_payload(alert_name, sensor_id, sensor_type, threshold, relation, alert_id)

    assert (payload["thresholds"][0]["value"] == threshold)
    assert (payload["thresholds"][0]["type"] == "lesser")

    relation = "<="
    payload =  influxdb.set_alert_payload(alert_name, sensor_id, sensor_type, threshold, relation, alert_id)

    assert (payload["thresholds"][0]["value"] == (threshold + 1))
    assert (payload["thresholds"][0]["type"] == "lesser")

    for tag in payload["query"]["builderConfig"]["tags"]:
        if tag["key"] == "sensor_id":
            assert tag["values"] == [sensor_id]
        if tag["key"] == "sensor_type":
            assert tag["values"] == [sensor_type]
