from flask import Flask, request, jsonify
import redis
import numpy as np

webapp = Flask(__name__)

class web_application:
    # * This class is used to create a web application that will receive the data from the sensor
    
    def __init__(self, url: str, port: int, debug: bool = False):
        self.url = url
        self.port = port
        self.debug = debug

    # TODO : fix the https status code 403 and add more url if needed
    @webapp.route('/new_data', methods=['POST'])
    def __receivesensor():
        data = request.json
        print(data)
        return jsonify(data)

    def runserver(self):
        webapp.run(host=self.url, port=self.port, debug=self.debug)
        

class redis_database:
    def __init__(self, host: str, port: int, db: int):
        self.host = host
        self.port = port
        self.db = db
        self.pool = None
        self.redisdb = None
        
    def connect(self):
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        self.redisdb = redis.Redis(connection_pool=self.pool)

class processing_data:
    # * This class is used to process the data from the sensor (how to process the data is not decided yet)
    
    def compute_avg(self,data: list()) -> float:
        return np.mean(data)

web_app = web_application("localhost", 5000, True)
web_app.runserver()