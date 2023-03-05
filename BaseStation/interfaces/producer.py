import time
import json

from kafka import KafkaProducer



producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    
def send_sensor_msg(sensor_msg, sensor_type, flush = False):
    sensor_stream = ''

    match sensor_type:
        case 'humidity sensor':
            sensor_stream = 'humidity_stream'
        case 'temperature sensor':
            sensor_stream = 'temperature_stream'
        case 'soil_moisture sensor':
            sensor_stream = 'soil_moisture_stream'
        case _:
            print('Sensor message error, unassigned stream')

    print('sending ', sensor_stream, sensor_msg)
    producer.send(sensor_stream, sensor_msg)
    if flush:
        producer.flush()

def send_task_msg(task_msg, flush = False):
    producer.send('task_stream', task_msg)
    if flush:
        producer.flush()

def send_rule_msg(rule_msg, flush = False):
    producer.send('rule_stream', rule_msg)
    if flush:
        producer.flush()
