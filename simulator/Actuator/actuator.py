import json
import time
import websockets
import asyncio
import threading



class Actuator:
    def __init__(self, id, states, event_handler, end_point):
        # define initial state and states
        self.end_point = end_point
        self.id = id
        self.states = [s.lower() for s in states]
        self.state = self.states[0]
        # event is what happen to change the state
        self.events = dict()
        # self.actions = {state: dict() for state in self.states}
        self.flag = False
        self.command = None
        self.threadSpare = True
        self.eve = threading.Event()
        self.thread = threading.Thread(target=self.threadCommandRunning)
        self.thread.start()
        for i, state in enumerate(states):
            self.events[state.lower()] = event_handler[i]


    def threadCommandRunning(self):
        self.flag = False
        while True:
            self.eve.wait()
            self.threadSpare = False
            # put the run command code here
            output = self.run(self.command)
            self.threadSpare = True
            self.eve.clear()
            if self.flag:
                break


    async def receive_commands(self):
        async with websockets.connect(self.end_point, ping_timeout = None) as ws:
            message = {
                "type" : "actuator",
                "status" : "OPEN_CONNECTION",
                "actuatorId": self.id,
                "actuatorType": "sprinkler"
            }
            await ws.send(json.dumps(message))
            while True:
                json_data = await ws.recv()
                data = json.loads(json_data)
                self.command = data["instruction"]
                self.eve.set()
                if not self.threadSpare:
                    self.threadSpare = True
                    self.thread.join()
                    self.thread = threading.Thread(target=self.threadCommandRunning)
                    self.thread.start()
                    self.eve.set()
                await ws.send(json.dumps({
                    "type": "ACKNOWLEDGEMENT",
                    "status": 'activate',
                    "actuatorId": self.id
                }))


    def _add_event(self, state, handler):
        self.events[state] = handler

    def run(self, input):
        new_state, output = self.events[self.state](input)
        # self.actions[self.state][new_state](output)
        self.state = new_state.lower()
        if self.flag:
            print("The action is interrupted")
        else:
            if self.state == "water" or self.state=="pump":
                self.state = "on"
            print("Current state is {}".format(self.state))
        return output


    # async def main(self):
    #     async with websockets.serve(self.receive_commands, "localhost", 8888):
    #         await asyncio.Future()  # run forever


   # def _add_action(self, cur_state, next_state, handler):
    #     self.actions[cur_state][next_state] = handler

   # async def receive_commands(self, websocket):
    #     message = {
    #         "actuator_id": self.id,
    #         "actuator_type": "sprinkler"
    #     }
    #     await websocket.send(json.dumps(message))
    #     while True:
    #         json_data = await websocket.recv()
    #         data = json.loads(json_data)
    #         print(f"Received JSON Data :{data}")
    #         commands = data["input"]
    #         output = await self.run(commands)
    #         back_data = {
    #             "actuator_id": self.id,
    #             "status": output
    #         }
    #         back_json_data = json.dumps(back_data)
    #         await websocket.send(back_json_data)