from flask import Flask, request, jsonify, json
import numpy as np
import aiohttp
from werkzeug.exceptions import HTTPException

webapp = Flask(__name__)

class edge_data_processor:
    # * This class is used to create a web application that will receive the data from the sensor
    
    def __init__(self, url: str, port: int, debug: bool = False):
        self.url = url
        self.port = port
        self.debug = debug

    @webapp.route('/new_data', methods=['POST'])
    async def __receivesensor() -> None:
        data = request.json
        print(data)
        data_buffer_connection.send_data(data)
                    
                    
        
    # * Handle the error
    @webapp.errorhandler(code_or_exception=HTTPException)
    def handle_exception(self,e) -> json:
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response


    def runserver(self) -> None:
        webapp.run(host=self.url, port=self.port, debug=self.debug)
        # TODO: Implement the code to send data back to main machine or other iot base station
        """
            pseudocode:
            while True:
                if sleep or timeout is finised:
                    if data in Redis is not empty: (If the existing dat is not sent):
                        get data from Redi
                        aggregate data
                        send data to main machine or other iot base station (if it could not reached the main machine) -> using aiohttp to send http request 
                    sleep or timeout
        """
        

class processing_data:
    # * This class is used to process the data from the sensor (how to process the data is not decided yet)
    def compute_avg(self,data: list()) -> float:
        return np.mean(data)

    def compute_min(self,data: list()) -> float:
        return np.min(data)
    
    def compute_max(self,data: list()) -> float:
        return np.max(data)

class data_buffer_connection:
    # * Send data to the data buffer
    async def send_data(self,data) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:23333/sensor", json=data) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Error while sending data to the DataBuffer: {resp.status}"
                    )
                    return f"Error while sending data to the DataBuffer: {resp.status}"
                else:
                    print(f"Data sent to DataBuffer: {data}")
                    return f"Data sent to DataBuffer: {data}"
    
    # * Get data from the data buffer
    async def get_data(self,sensor_id: str, timestamp: str) -> json:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:23333/sensor", sensor_id=sensor_id,timestamp=timestamp) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Error while getting data from the DataBuffer: {resp.status}"
                    )
                    return f"Error while getting data from the DataBuffer: {resp.status}"
                else:
                    print(f"Data received from DataBuffer: {resp.json()}")
                    return resp.json()
    # * Delete data from the data buffer (in case that the data is sent to the main machine)
    async def delete_data(self,sensor_id: str, timestamp: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"http://localhost:23333/sensor", sensor_id=sensor_id,timestamp=timestamp) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Error while deleting data from the DataBuffer: {resp.status}"
                    )
                    return f"Error while deleting data from the DataBuffer: {resp.status}"
                else:
                    print(f"Data deleted from DataBuffer: {resp.json()}")
                    return f"Data deleted from DataBuffer: {resp.json()}"

web_app = edge_data_processor("localhost", 5500, True)
web_app.runserver()