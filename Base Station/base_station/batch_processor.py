from pathlib import Path
import csv

script_location = Path(__file__).absolute().parent
cold_store_file = script_location / 'local_data/sensor_data_cold_store.csv'

def store_locally(batch):
    with open(cold_store_file, 'a', newline='', encoding='utf8') as f:
        for entry in batch:
            entry = entry.asdict()
            writer = csv.DictWriter(f, entry.keys())
            writer.writerow(entry)