import time
import json

from kafka import KafkaProducer



producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: json.dumps(x).encode('utf-8'))

humidity_msg = {'sensor_id':'test_sensor1', 'reading':60}
temperature_msg = {'sensor_id':'test_sensor2', 'reading':20}
soil_moisture_msg = {'sensor_id':'test_sensor3', 'reading':10}

for i in range(2):
    time.sleep(1)
    producer.send('humidity_stream', humidity_msg)
    producer.send('temperature_stream', temperature_msg)
    producer.send('soil_moisture_stream', soil_moisture_msg)
    