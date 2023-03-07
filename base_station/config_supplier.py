from pathlib import Path
from configparser import ConfigParser

script_location = Path(__file__).absolute().parent
file_location = script_location / 'configs/base_station.ini'

configur = ConfigParser()

configurations = {}

try:
  configur.read(file_location)
  #print ("Sections : ", configur.sections())
  batch_configs = configur['batch']
  for config in batch_configs:
    configurations[config] = batch_configs[config]
except Exception as e:
  print(e)

def get_configs():
  return configurations