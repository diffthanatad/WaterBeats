from actuator import Actuator
import time
import asyncio


class Pump(Actuator):
    def __init__(self, id, end_point):
        self.states = ["ON", "OFF", "PUMP"]
        self.events_handler = [self.onHandler, self.offHandler, self.pumpHandler]
        super().__init__(id, self.states, self.events_handler, end_point)

    # event handler for ON state
    # combine state change and actions to the same function
    def onHandler(self, input):
        if input == 'pumping':
            print("the pump is pumping")
            self.pumping(10)
            return ("PUMP", "on")
        elif input == 'off':
            print("the pump is off")
            return ("OFF", "on")
        else:
            print("WRONG COMMAND, the pump turn to OFF")
            return ("OFF", "error")

    # event handler for off state
    def offHandler(self, input):
        if input == 'on':
            print("the pump is on")
            return ("ON", "on")
        else:
            print("WRONG COMMAND, the pump turn to OFF")
            return ("OFF", "error")

    # event handler for pump state
    def pumpHandler(self, input):
        if input == 'off':
            print("the pump is off")
            return ("OFF", "on")
        elif input == 'pumping':
            print("the pump is pumping again")
            self.pumping(10)
            return ("ON", "on")
        else:
            print("WRONG COMMAND, the pump turn to OFF")
            return ("OFF", "error")

    def pumping(self, dur):
        print("pumping time is {}".format(dur))
        for i in range(dur):
            if self.threadSpare:
                self.flag = True
                break
            time.sleep(1)
            print("time remains {}".format(dur-i))


if __name__ == '__main__':
    pump = Pump(1, "ws://localhost:8765")
    asyncio.run(pump.receive_commands())