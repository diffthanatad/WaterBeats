import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import producer as p

from flask import Flask, request
from flask_cors import CORS

from waitress import serve



app = Flask(__name__)
CORS(app)

@app.post("/rules_data/send_rules")
def handle_request():
    try:
        # get data from request
        data = {
            'actuator_id': request.args.get("actuator_id"),
            'actuator_type': request.args.get("actuator_type"),
            'actuator_state': request.args.get("actuator_state"),
            'intensity': request.args.get("intensity"),
            'duration': request.args.get("duration"),
            'subject_sensor': request.args.get("subject_sensor"),
            'sensor_condition': request.args.get("reading"),
            'condition_relation': request.args.get("relation")
        }
        # reformat data
        data['intensity'] = 1.0
        data['duration'] = float(data['duration'])
        data['sensor_condition'] = float(data['sensor_condition'])
        data['actuator_state'] = True if data['actuator_state'] == 'True' else False

        # reconstruct rule message
        task_message = {'actuator_target':data['actuator_id'], 'state':data['actuator_state'], 'intensity':data['intensity'], 'duration': data['duration']}
        sensor_condition_message = {'sensor_subject':data['subject_sensor'], 'reading':data['sensor_condition'], 'relation':data['condition_relation']}
        rule_message = {'task_message':task_message, 'sensor_condition_message' : sensor_condition_message}

        # send rule message
        p.send_rule_msg(rule_message, True)

        return { 'data': data }, 200
    except Exception as e:
        return { 'error': str(e)}, 500
    

@app.get("/rules_data")
def test():
    try:
        return { 'data': 'Hello' }, 200
    except Exception as e:
        return { 'error': str(e) }, 500


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=23334)