from flask import Flask, request, jsonify, json
import asyncio
from werkzeug.exceptions import HTTPException
import json
from data_buffer_connection import data_buffer_connection

webapp = Flask(__name__)

class edge_data_processor:
    # * This class is used to create a web application that will receive the data from the sensor
    
    def __init__(self, url: str, port: int, debug: bool = False):
        self.url = url
        self.port = port
        self.debug = debug

    # * This function is used to receive the data from the sensor
    @webapp.route('/new_data', methods=['POST'])
    async def __receivesensor() -> None:
        data = request.json
        print(data)
        await data_buffer_connection.send_data(data)
        return("OK", 201)
                    
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

    # * This function is used to run the web application
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


if __name__ == "__main__":
    webserver = edge_data_processor("localhost", 5500, True)
    webserver.runserver()