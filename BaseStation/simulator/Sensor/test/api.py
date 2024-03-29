from flask import Flask, request, json
from werkzeug.exceptions import HTTPException
# from data_management import DataManagement, insert_sensor_data, insert_actuator_data
# from create_token import find_waterbeats_buckets, create_token_for_bucket

webapp = Flask(__name__)

class server:
    
    def __init__(self, url: str, port: int, debug: bool = False):
        self.url = url
        self.port = port
        self.debug = debug
        
    @webapp.route('/sensor_data', methods=['POST'])
    def __receive_sensor_data() -> tuple:
        data = request.json
        # sensor_id = data['sensor_id']
        # sensor_type = str(data['sensor_type'])
        # sensor_data = float(data['data'])
        # unit = str(data['unit'])
        # longitude = float(data['longitude'])
        # latitude = float(data['latitude'])
        # timestamp = int(data['timestamp'])
        print(data)
        return ('', 200)

    @webapp.route('/actuator_data', methods=['POST'])
    def __receive_actuator_data() -> tuple:
        data = request.json
        try:
    #         actuator_id = str(data['actuator_id'])
    #         actuator_type = str(data['actuator_type'])
    #         actuator_status= str(data['status'])
    #         longitude = float(data['longitude'])
    #         latitude = float(data['latitude'])
    #         timestamp = int(data['timestamp'])
    #         wb_bucket = find_waterbeats_buckets()
    #         wb_token = create_token_for_bucket(wb_bucket["id"],wb_bucket["orgID"])
    #         wb_datamangement = DataManagement(wb_bucket["id"], wb_bucket["orgID"], wb_token, "http://localhost:8086")
            try :
    #             insert_actuator_data(wb_datamangement, actuator_id, actuator_type, actuator_status, longitude, latitude, timestamp)
                print(data)
                return ('', 200)
            except Exception as e:
                return (f"Error while inserting data to the DataBuffer: {e}", 500)
        except KeyError as k:
            return (f"Some data is missing: {k}", 400)
        except Exception as e:
            return (f"Error: {e}", 500)
        
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

if __name__ == "__main__":
    webserver = server("localhost", 5555, True)
    webserver.runserver()