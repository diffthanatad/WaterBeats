from actuator import Actuator
import time
import asyncio


class Sprinkler(Actuator):
    def __init__(self, id, end_point):
        self.states = ["ON", "OFF", "WATER"]
        self.events_handler = [self.onHandler, self.offHandler, self.waterHandler]
        super().__init__(id, self.states, self.events_handler, end_point)

    # event handler for ON state
    # combine state change and actions to the same function
    def onHandler(self, input):
        if input == 'watering':
            print("the sprinkler is watering")
            self.watering(10)
            return ("WATER", "on")
        elif input == 'off':
            print("the sprinkler is off")
            return ("OFF", "on")
        else:
            print("WRONG COMMAND, the sprinkler ture to OFF")
            return ("OFF", "error")

    # event handler for off state
    def offHandler(self, input):
        if input == 'on':
            print("the sprinkler is on")
            return ("ON", "on")
        else:
            print("WRONG COMMAND, the sprinkler ture to OFF")
            return ("OFF", "error")

    # event handler for water state
    def waterHandler(self, input):
        if input == 'off':
            print("the sprinkler is off")
            return ("OFF", "on")
        elif input == 'watering':
            print("the sprinkler is watering again")
            self.watering(10)
            return ("ON", "on")
        else:
            print("WRONG COMMAND, the sprinkler ture to OFF")
            return ("OFF", "error")

    def watering(self, dur):
        print("watering time is {}".format(dur))
        for i in range(dur):
            if self.threadSpare:
                self.flag = True
                break
            time.sleep(1)
            print("time remains {}".format(dur-i))


if __name__ == '__main__':
    sprinkler = Sprinkler('F4:12:FA:83:00:F0_D', "ws://localhost:8765")
    asyncio.run(sprinkler.receive_commands())