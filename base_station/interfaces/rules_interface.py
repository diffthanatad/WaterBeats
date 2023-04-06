import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import producer as p
import records

from flask import Flask, request
from flask_cors import CORS

from waitress import serve



app = Flask(__name__)
CORS(app)

@app.post("/rules_data/send_rules")
def handle_request():
    try:
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
        print('actuator_id', data['actuator_id'])
        print(data)
        task_message = records.TaskMessage(data['actuator_id'], data['actuator_state'], data['intensity'], data['actuator_type'], data['duration'])
        sensor_condition_message = records.SensorConditionMessage(data['subject_sensor'], data['sensor_condition'], data['condition_relation'])
        rule_message = records.RuleMessage(task_message, sensor_condition_message, None)
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
    # app.run(debug=True, host="0.0.0.0")