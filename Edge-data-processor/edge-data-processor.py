from flask import Flask, request, jsonify, json
import redis
import numpy as np
from aiohttp import web
from werkzeug.exceptions import HTTPException

webapp = Flask(__name__)

class edge_data_processor:
    # * This class is used to create a web application that will receive the data from the sensor
    
    def __init__(self, url: str, port: int, debug: bool = False):
        self.url = url
        self.port = port
        self.debug = debug

    @webapp.route('/new_data', methods=['POST'])
    def __receivesensor():
        # !: Databuffer component is not implemented yet
        data = request.json
        print(data)
        return jsonify(data)

    # * Handle the error
    @webapp.errorhandler(code_or_exception=HTTPException)
    def handle_exception(self,e):
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response


    def runserver(self):
        webapp.run(host=self.url, port=self.port, debug=self.debug)
        # TODO: Implement the code to send data back to main machine or other iot base station
        """
            pseudocode:
            while True:
                if sleep or timeout is finised:
                    if data in Redis is not empty: (If the existing dat is not sent):
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


web_app = web_application("localhost", 5500, True)
web_app.runserver()