import os
import json
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from psycopg2.extras import RealDictCursor
from twilio.rest import Client
from flask_cors import CORS

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

class Alerts:
    @app.get("/alert/getAllAlerts")
    def get_all_alerts():
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM alerts")
                alerts = cursor.fetchall()

        return { 'data': alerts }, 200

    @app.get("/alert/getAlertBySensorId")
    def get_alert_by_sensor_id():
        sensor_id = request.args.get("sensor_id")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(f"SELECT * FROM alerts WHERE sensor_id = '{sensor_id}'")
                alerts = cursor.fetchall()

        return { 'data': alerts }, 200

    @app.post("/alert/addAlert")
    def add_alert():
        sensor_id = request.args.get("sensor_id")
        sensor_type = request.args.get("sensor_type")
        threshold = request.args.get("threshold")
        relation = request.args.get("relation")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "INSERT INTO alerts (sensor_id, sensor_type, threshold, relation)" \
                    f"VALUES ('{sensor_id}', '{sensor_type}', '{threshold}', '{relation}') RETURNING sensor_id"
                )
                sensor_id = cursor.fetchone()

        return { 'data': sensor_id }, 200

    @app.put("/alert/updateAlertBySensorId")
    def update_alert_by_sensor_id():
        sensor_id = request.args.get("sensor_id")
        threshold = request.args.get("threshold")
        relation = request.args.get("relation")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    f"UPDATE alerts SET threshold = '{threshold}', relation = '{relation}' " \
                    f"WHERE sensor_id = '{sensor_id}' RETURNING sensor_id"
                )
                sensor_id = cursor.fetchone()

        return { 'data': sensor_id }, 200

    @app.delete("/alert/deleteAlertBySensorId")
    def delete_alert_by_sensor_id():
        sensor_id = request.args.get("sensor_id")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM alerts " \
                    f"WHERE sensor_id = '{sensor_id}' RETURNING sensor_id"
                )
                sensor_id = cursor.fetchone()

        return { 'data': sensor_id }, 200

    @app.post("/alert/sendAlert")
    def send_alert():
        account_sid = "AC0b2beb8a125692224e8fce035e48ce5e"
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        body="\n\nALERT:\n\n Sensor is greater than threshold!",
        from_="+447883318669",
        to="+447846927467"
        )

        return "Success", 200

class Rules:

    @app.get("/rule/getAllRules")
    def get_all_rules():
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM rules")
                rules = cursor.fetchall()

        return { 'data': rules }, 200

    @app.get("/rule/getRuleByActuatorId")
    def get_rule_by_actuator_id():
        actuator_id = request.args.get("actuator_id")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(f"SELECT * FROM rules WHERE actuator_id = '{actuator_id}'")
                rule = cursor.fetchone()

        return { 'data': rule }, 200

    @app.post("/rule/addRule")
    def add_rule():
        subject_sensor = request.args.get("subject_sensor")
        sensor_reading = request.args.get("sensor_reading")
        relation = request.args.get("relation")
        actuator_id = request.args.get("actuator_id")
        actuator_type = request.args.get("actuator_type")
        actuator_state = request.args.get("actuator_state")
        intensity = request.args.get("intensity")
        duration = request.args.get("duration")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    f"INSERT INTO rules (subject_sensor, sensor_reading, relation, actuator_id, \
                    actuator_type, actuator_state, intensity, duration) \
                    VALUES ('{subject_sensor}', '{sensor_reading}', '{relation}', '{actuator_id}',  \
                    '{actuator_type}', '{actuator_state}', '{intensity}', '{duration}') \
                    RETURNING actuator_id"
                )
                actuator_id = cursor.fetchone()

        return { 'data': actuator_id }, 200

    @app.put("/rule/updateRuleByActuatorId")
    def update_rule_by_actuator_id():
        subject_sensor = request.args.get("subject_sensor")
        sensor_reading = request.args.get("sensor_reading")
        relation = request.args.get("relation")
        actuator_id = request.args.get("actuator_id")
        actuator_state = request.args.get("actuator_state")
        intensity = request.args.get("intensity")
        duration = request.args.get("duration")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    f"UPDATE rules SET subject_sensor = '{subject_sensor}', sensor_reading = '{sensor_reading}', \
                    relation = '{relation}', actuator_id = '{actuator_id}', actuator_state = '{actuator_state}', \
                    intensity = '{intensity}', duration = '{duration}' \
                    WHERE actuator_id = '{actuator_id}' RETURNING actuator_id"
                )
                actuator_id = cursor.fetchone()

        return { 'data': actuator_id }, 200

    @app.delete("/rule/deleteRuleByActuatorId")
    def delete_rule_by_actuator_id():
        actuator_id = request.args.get("actuator_id")

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM rules " \
                    f"WHERE actuator_id = '{actuator_id}' RETURNING actuator_id"
                )
                actuator_id = cursor.fetchone()

        return { 'data': actuator_id }, 200

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=3001)
