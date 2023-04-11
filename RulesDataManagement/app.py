import os
import psycopg2
import requests
import sys

from dotenv import load_dotenv
from flask import Flask, request, abort
from flask_cors import CORS
from influxdb import InfluxDB
from psycopg2.extras import RealDictCursor
from twilio.rest import Client


load_dotenv()
app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(
    dbname=os.getenv("RULES_DB_NAME"),
    user=os.getenv("RULES_DB_USER"),
    password=os.getenv("RULES_DB_PASSWORD"),
    host=os.getenv("RULES_DB_HOST"),
    port=os.getenv("RULES_DB_PORT")
)
RULES_BACKEND_URL = os.getenv("RULES_BACKEND_URL")
influxdb = InfluxDB()

class Alerts:

    @app.get("/alert/getAllAlerts")
    def get_all_alerts():
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM alerts")
                db_alerts = cursor.fetchall()

        return { "data": db_alerts }, 200


    @app.get("/alert/getAlertBySensorId")
    def get_alert():
        sensor_id = request.args.get("sensor_id")

        if not sensor_id:
            abort(400, "Required parameter missing: sensor_id")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(f"SELECT * FROM alerts WHERE sensor_id = '{sensor_id}'")
                db_alert = cursor.fetchone()

        return { "data": db_alert }, 200


    @app.post("/alert/addAlert")
    def add_alert():
        threshold = None if not request.args.get("threshold") else int(request.args.get("threshold"))
        data = {
            "sensor_id": request.args.get("sensor_id"),
            "sensor_type": request.args.get("sensor_type"),
            "threshold": threshold,
            "relation": request.args.get("relation")
        }
        error_message = "Required parameter missing: "
        {abort(400, error_message + k) for k, v in data.items() if not v}

        alert_id = influxdb.create_alert(data["sensor_id"], data["sensor_type"], data["threshold"], data["relation"])
        if not alert_id:
            abort(500, "Failed to create alert in InfluxDB")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    f"INSERT INTO alerts (sensor_id, sensor_type, threshold, relation) \
                    VALUES ('{data['sensor_id']}', '{data['sensor_type']}', '{data['threshold']}', '{data['relation']}') \
                    ON CONFLICT (sensor_id) DO NOTHING RETURNING sensor_id"
                )
                db_sensor_id = cursor.fetchone()

        if not db_sensor_id:
            abort(400, "Required parameter already exists: sensor_id")

        return { "data": db_sensor_id }, 201


    @app.put("/alert/updateAlertBySensorId")
    def update_alert():
        threshold = None if not request.args.get("threshold") else int(request.args.get("threshold"))
        data = {
            "sensor_id": request.args.get("sensor_id"),
            "sensor_type": request.args.get("sensor_type"),
            "threshold": threshold,
            "relation": request.args.get("relation")
        }
        error_message = "Required parameter missing: "
        {abort(400, error_message + k) for k, v in data.items() if not v}

        is_updated = influxdb.update_alert(data["sensor_id"], data["sensor_type"], data["threshold"], data["relation"])
        if not is_updated:
            abort(500, "Failed to update alert in InfluxDB")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    f"UPDATE alerts SET threshold = '{data['threshold']}', relation = '{data['relation']}' \
                    WHERE sensor_id = '{data['sensor_id']}' RETURNING sensor_id"
                )
                db_sensor_id = cursor.fetchone()

        if not db_sensor_id:
            abort(400, "Required parameter invalid: sensor_id")

        return { "data": db_sensor_id }, 200


    @app.delete("/alert/deleteAlertBySensorId")
    def delete_alert():
        sensor_id = request.args.get("sensor_id")

        if not sensor_id:
            abort(400, "Required parameter missing: sensor_id")

        is_deleted = influxdb.delete_alert(sensor_id)
        if not is_deleted:
            abort(500, "Failed to delete alert in InfluxDB")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    f"DELETE FROM alerts \
                    WHERE sensor_id = '{sensor_id}' RETURNING sensor_id"
                )
                db_sensor_id = cursor.fetchone()

        if not db_sensor_id:
            abort(400, "Required parameter invalid: sensor_id")

        return { "data": db_sensor_id }, 200


    @app.post("/alert/sendAlert")
    def send_alert():
        account_sid = os.getenv("TWILIO_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="\n\nALERT TRIGGERED:\n\n Sensor is greater than threshold!",
            from_=os.getenv("TWILIO_FROM_NUMBER"),
            to=os.getenv("TWILIO_TO_NUMBER")
        )
        return "Success", 200


class Rules:

    @app.get("/rule/getAllRules")
    def get_all_rules():
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM rules")
                db_rules = cursor.fetchall()

        return { "data": db_rules }, 200


    @app.get("/rule/getRuleByActuatorId")
    def get_rule():
        actuator_id = request.args.get("actuator_id")

        if not actuator_id:
            abort(400, "Required parameter missing: actuator_id")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(f"SELECT * FROM rules WHERE actuator_id = '{actuator_id}'")
                db_rule = cursor.fetchone()

        return { "data": db_rule }, 200


    @app.post("/rule/addRule")
    def add_rule():
        data = {
            "subject_sensor": request.args.get("subject_sensor"),
            "sensor_reading": request.args.get("sensor_reading"),
            "relation": request.args.get("relation"),
            "actuator_id": request.args.get("actuator_id"),
            "actuator_type": request.args.get("actuator_type"),
            "actuator_state": request.args.get("actuator_state"),
            "intensity": request.args.get("intensity"),
            "duration": request.args.get("duration")
        }
        error_message = "Required parameter missing: "
        {abort(400, error_message + k) for k, v in data.items() if not v}

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    f"INSERT INTO rules (subject_sensor, sensor_reading, relation, actuator_id, \
                    actuator_type, actuator_state, intensity, duration) \
                    VALUES ('{data['subject_sensor']}', '{data['sensor_reading']}', '{data['relation']}', '{data['actuator_id']}',  \
                    '{data['actuator_type']}', '{data['actuator_state']}', '{data['intensity']}', '{data['duration']}') \
                    ON CONFLICT (actuator_id) DO NOTHING RETURNING actuator_id"
                )
                db_actuator_id = cursor.fetchone()

        if not db_actuator_id:
            abort(400, "Required parameter already exists: actuator_id")

        try:
            requests.post(RULES_BACKEND_URL, params=data, headers = {"Content-Type": "application/json"})
        except:
            pass

        return { "data": db_actuator_id }, 201


    @app.put("/rule/updateRuleByActuatorId")
    def update_rule():
        data = {
            "subject_sensor": request.args.get("subject_sensor"),
            "sensor_reading": request.args.get("sensor_reading"),
            "relation": request.args.get("relation"),
            "actuator_id": request.args.get("actuator_id"),
            "actuator_state": request.args.get("actuator_state"),
            "intensity": request.args.get("intensity"),
            "duration": request.args.get("duration")
        }
        error_message = "Required parameter missing: "
        {abort(400, error_message + k) for k, v in data.items() if not v}

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    f"UPDATE rules SET subject_sensor = '{data['subject_sensor']}', sensor_reading = '{data['sensor_reading']}', \
                    relation = '{data['relation']}', actuator_id = '{data['actuator_id']}', actuator_state = '{data['actuator_state']}', \
                    intensity = '{data['intensity']}', duration = '{data['duration']}' \
                    WHERE actuator_id = '{data['actuator_id']}' RETURNING actuator_id"
                )
                db_actuator_id = cursor.fetchone()

        if not db_actuator_id:
            abort(400, "Required parameter invalid: actuator_id")

        return { "data": db_actuator_id }, 200


    @app.delete("/rule/deleteRuleByActuatorId")
    def delete_rule():
        actuator_id = request.args.get("actuator_id")

        if not actuator_id:
            abort(400, "Required parameter missing: actuator_id")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    f"DELETE FROM rules \
                    WHERE actuator_id = '{actuator_id}' RETURNING actuator_id"
                )
                db_actuator_id = cursor.fetchone()

        if not db_actuator_id:
            abort(400, "Required parameter invalid: actuator_id")

        return { "data": db_actuator_id }, 200


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=3001)
