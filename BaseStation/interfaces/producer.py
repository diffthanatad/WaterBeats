import time
import json

from kafka import KafkaProducer



producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    
def send_sensor_msg(sensor_msg, flush = False):
    print('Producer sending sensor message', sensor_msg)
    producer.send('sensor_stream', sensor_msg)
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
