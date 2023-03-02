import time
import json

from kafka import KafkaProducer



producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: json.dumps(x).encode('utf-8'))

def send_humidity_msg(humidity_msg, flush = False):
    producer.send('humidity_stream', humidity_msg)
    if flush:
        producer.flush()
    
def send_temperature_msg(temperature_msg, flush = False):
    producer.send('temperature_stream', temperature_msg)
    if flush:
        producer.flush()
    
def send_soil_moisture_msg(soil_moisture_msg, flush = False):
    producer.send('soil_moisture_stream', soil_moisture_msg)
    if flush:
        producer.flush()



humidity_msg = {'sensor_id':'test_sensor1', 'reading':60}
temperature_msg = {'sensor_id':'test_sensor2', 'reading':20}
soil_moisture_msg = {'sensor_id':'test_sensor3', 'reading':10}

send_humidity_msg(humidity_msg, True)
send_temperature_msg(temperature_msg, True)
send_soil_moisture_msg(soil_moisture_msg, True)