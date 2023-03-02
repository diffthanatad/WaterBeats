class Task:
    """Tasks for an actuator

    Attributes:
        target      The actuatorid/target to control
        state       The intended on/off state of the instruction to the target
        intensity   E.g., rotational speed of motor, pressure of sprinkler. Between 0 and 1.
        duration    Optional duration until reversion to previous state in seconds. -1 for indefinite duration.
    """

    def __init__(self, target: str, state: str, intensity: float, duration: int):
        self.target = target
        self.state = state
        self.intensity = intensity
        self.duration = duration
    
    def __str__(self):
        return(f"Task({self.target}, {self.state}, {self.intensity}, {self.duration})")

class Rule:
    def __init__(self, task: Task):
        self.task = task

# conditionTime = datetime.datetime.now() + datetime.timedelta(seconds=10)

# condition1 = Condition(conditionTime, False, 'test_sensor3', 20, '<')

def analyse(message):
    tasks = []
    # check conditions of rules are met
    # return list of applicable tasks
    return tasks