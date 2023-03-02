import base_station as bs
import rule_engine as re
import device_controller as dc



# send to rule engine and retrieve applicable tasks
async def process(message):
    tasks = re.analyse(message)
    for task in tasks:
        actuator_data = dc.getActuatorData(task.target)
        task_msg = bs.TaskMessage(task.target, actuator_data.device_type, task.state, task.intensity, task.duration)

        await bs.task_stream.send(value=task_msg)



# forward to main hub
def sendToHub(message):
    pass
