import producer as p
import time



task1 = {'actuator_target':'test_actuator1', 'state':True, 'intensity':0.1, 'duration': 10}
condition1 = {'sensor_subject':'test_sensor1', 'reading':20, 'relation':'<'}
rule1 = {'task_message':task1, 'condition_message': condition1}

p.send_rule_msg(rule1, True)

time.sleep(5)

humidity_msg = {'sensor_id':'test_sensor1', 'reading':25}
p.send_sensor_msg(humidity_msg, 'humidity sensor', True)

humidity_msg = {'sensor_id':'test_sensor1', 'reading':20}
p.send_sensor_msg(humidity_msg, 'humidity sensor', True)

humidity_msg = {'sensor_id':'test_sensor1', 'reading':15}
p.send_sensor_msg(humidity_msg, 'humidity sensor', True)




# p.send_sensor_msg(humidity_msg, 'humidity sensor', True)
# p.send_sensor_msg(temperature_msg, 'temperature sensor', True)
# p.send_sensor_msg(soil_moisture_msg, 'soil_moisture sensor', True)

# task_msg = {'actuator_target':'test_actuator1', 'state':True, 'intensity':0.5, 'duration':10}

# p.send_task_msg(task_msg, True)