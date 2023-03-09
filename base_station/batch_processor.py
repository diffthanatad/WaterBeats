from pathlib import Path
import time
import csv

script_location = Path(__file__).absolute().parent
humidity_f = script_location / 'local_data/humidity_cold_store.csv'
temperature_f = script_location / 'local_data/temperature_cold_store.csv'
soil_moisture_f = script_location / 'local_data/soil_moisture_cold_store.csv'

def get_timestamp():
  return time.strftime('%Y-%m-%d %H:%M:%S')

def store_locally(batch):
    data_type = batch[0].sensor_type
    if data_type == 'humidity sensor':
        cold_store_f = humidity_f
    elif data_type == 'temperature sensor':
        cold_store_f = temperature_f
    else:
        cold_store_f = soil_moisture_f

    with open(cold_store_f, 'a', newline='', encoding='utf8') as f:
        for entry in batch:
            entry = entry.asdict()
            writer = csv.DictWriter(f, entry.keys())
            writer.writerow(entry)
    print('sensor data batch stored successfully @ ' + get_timestamp())