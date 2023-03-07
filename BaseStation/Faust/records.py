import faust

### defines channel message types
# sensor message - sensor data, e.g. humidity reading
class SensorMessage(faust.Record):
    sensor_id: str
    reading: float
    sensor_type: str = ''
    reading_unit: str = ''
    timestamp: str = ''
    latitude: float = ''
    longitude: float = ''

# task message - tasks to execute immediately, e.g. turn actuator off right now
class TaskMessage(faust.Record):
    actuator_target: str
    state: bool
    intensity: float
    actuator_type: str = ''
    duration: int = -1

    def toDict(self):
        return {
            'actuator_target' : self.actuator_target,
            'state' : self.state,
            'intensity': self.intensity,
            'actuator_type': self.actuator_type,
            'duration': self.duration,
            }

# condition message - conditions belonging to rules
class ConditionMessage(faust.Record):
    sensor_subject: str
    reading: float
    relation: str

    def toDict(self):
        return {
            'sensor_subject' : self.sensor_subject,
            'reading' : self.reading,
            'relation': self.relation,
            }

# rule message - complex rules that match tasks to conditions
class RuleMessage(faust.Record):
    task_message: TaskMessage
    condition_message: ConditionMessage = None