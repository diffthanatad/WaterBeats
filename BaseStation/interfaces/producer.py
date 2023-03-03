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



humidity_msg = {'sensor_id':'test_sensor1', 'reading':60}
temperature_msg = {'sensor_id':'test_sensor2', 'reading':20}
soil_moisture_msg = {'sensor_id':'test_sensor3', 'reading':10}

#send_humidity_msg(humidity_msg, True)
#send_temperature_msg(temperature_msg, True)
#send_soil_moisture_msg(soil_moisture_msg, True)

task_msg = {'actuator_target':'test_actuator1', 'state':True, 'intensity':0.5, 'duration':10}

send_task_msg(task_msg, True)