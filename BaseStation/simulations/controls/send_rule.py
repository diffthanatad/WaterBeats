import time
import json

from kafka import KafkaProducer



producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: json.dumps(x).encode('utf-8'))

def send_rule_msg(rule_msg, flush = False):
    producer.send('rule_stream', rule_msg)
    if flush:
        producer.flush()



#rule_msg = {}

#send_rule_msg(rule_msg, True)