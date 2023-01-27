import json
import time
import websockets
import asyncio

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
        for i, state in enumerate(states):
            self.events[state.lower()] = event_handler[i]

    # async def send_information(self, data):
    #     async with websockets.connect(self.end_point) as websocket:
    #         json_data = json.dumps(data)
    #         await websocket.send(json_data)
    #         receive_message = await websocket.recv()
    #         print(receive_message)

    def _add_event(self, state, handler):
        self.events[state] = handler

    # def _add_action(self, cur_state, next_state, handler):
    #     self.actions[cur_state][next_state] = handler

    async def run(self, input):
        new_state, output = self.events[self.state](input)
        # self.actions[self.state][new_state](output)
        self.state = new_state.lower()
        print("Current state is {}".format(self.state))
        return output

    async def receive_commands(self, websocket):
        message = {
            "actuator_id": self.id,
            "actuator_type": "sprinkler"
        }
        await websocket.send(json.dumps(message))
        while True:
            json_data = await websocket.recv()
            data = json.loads(json_data)
            print(f"Received JSON Data :{data}")
            commands = data["input"]
            output = await self.run(commands)
            back_data = {
                "actuator_id": self.id,
                "status": output
            }
            back_json_data = json.dumps(back_data)
            await websocket.send(back_json_data)

    async def main(self):
        async with websockets.serve(self.receive_commands, "localhost", 8888):
            await asyncio.Future()  # run forever




