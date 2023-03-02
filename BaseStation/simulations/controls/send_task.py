import time
import json

from kafka import KafkaProducer



producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: json.dumps(x).encode('utf-8'))

def send_task_msg(task_msg, flush = False):
    producer.send('task_stream', task_msg)
    if flush:
        producer.flush()



task_msg = {'actuator_target':'test_actuator1', 'state':True, 'intensity':0.5, 'duration':10}

send_task_msg(task_msg, True)