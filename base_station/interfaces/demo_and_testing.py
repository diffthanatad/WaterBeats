import producer as p
import time
import datetime

def get_timestamp():
    timestamp = datetime.datetime.now()
    timestamp = timestamp.replace(second = 0, microsecond = 0)
    return timestamp


task1 = {'actuator_target':'F4:12:FA:83:00:F0_D', 'state':True, 'intensity':0.1, 'duration': 10}
condition1 = {'sensor_subject':'30:AE:A4:14:C2:90_A', 'reading':20, 'relation':'<'}
rule1 = {'task_message':task1, 'condition_message': condition1}

task2 = {'actuator_target':'F4:12:FA:83:00:F0_D', 'state':True, 'intensity':0.1, 'duration': 10}
sensor_condition2 = {'sensor_subject':'F4:12:FA:83:00:F0_A', 'reading':23, 'relation':'>'}
future_time = str(get_timestamp() + datetime.timedelta(minutes = 1))
time_condition2 = {'execute_time': future_time}
#print('time now', get_timestamp(), 'time future', future_time)
#rule2 = {'task_message':task2, 'sensor_condition_message': sensor_condition2, 'time_condition_message': time_condition2}
rule2 = {'task_message':task2, 'sensor_condition_message': sensor_condition2, 'time_condition_message': time_condition2}
rule3 = {'task_message':task2, 'sensor_condition_message' : sensor_condition2}
rule4 = {'task_message':task2}

# p.send_rule_msg(rule3, True)

# time.sleep(5)

test_sensor1 = '30:AE:A4:14:C2:90_A'
test_sensor2 = 'F4:12:FA:83:00:F0_A'


humidity_msg = {'sensor_id': test_sensor2, 'reading':15}
p.send_sensor_msg(humidity_msg, True)


# task_msg = {'actuator_target':'test_actuator1', 'state':True, 'intensity':0.5, 'duration':10}

# p.send_task_msg(task_msg, True)