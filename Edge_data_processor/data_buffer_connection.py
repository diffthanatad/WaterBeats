import aiohttp
import json

class data_buffer_connection:
    @staticmethod
    async def send_data(data) -> str:
        print(data)
        """send data to the data buffer

        Args:
            data (json): json data

        Raises:
            Exception: Error while sending data to the DataBuffer

        Returns:
            str: Data sent to DataBuffer
        """
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:23333/sensor", json=data) as resp:
                if resp.status != 201:
                    raise Exception(
                        f"Error while sending data to the DataBuffer: {resp.status}"
                    )
                    return f"Error while sending data to the DataBuffer: {resp.status}"
                else:
                    print(f"Data sent to DataBuffer: {data}")
                    return f"Data sent to DataBuffer: {data}"
    
    @staticmethod
    async def get_data(sensor_id: str, timestamp: int) -> json:
        """get data from the data buffer

        Args:
            sensorId (str): sensor id
            timestamp (str): timestamp

        Raises:
            Exception: Error while getting data from the DataBuffer

        Returns:
            json: data of the specific sensor id and timestamp
        """
        async with aiohttp.ClientSession() as session:
            params = {"sensorId": sensor_id, "timestamp": timestamp}
            async with session.get(f"http://localhost:23333/sensor", params=params) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Error while getting data from the DataBuffer: {resp.status}"
                    )
                    return f"Error while getting data from the DataBuffer: {resp.status}"
                else:
                    response = await resp.json()
                    print(f"Data received from DataBuffer: {response['data']}")
                    return response['data']
    
    @staticmethod
    async def delete_data(sensor_id: str, timestamp: int) -> str:
        """delete data from the data buffer (in case that the data is sent to the main machine)

        Args:
            sensorId (str): sensor id
            timestamp (str): timestamp

        Raises:
            Exception: Error while deleting data from the DataBuffer

        Returns:
            str: Data deleted from DataBuffer
        """
        async with aiohttp.ClientSession() as session:
            params = {"sensorId": sensor_id, "timestamp": timestamp}
            async with session.delete(f"http://localhost:23333/sensor", params=params) as resp:
                if resp.status != 204 and resp.status != 202:
                    raise Exception(
                        f"Error while deleting data from the DataBuffer: {resp.status}"
                    )
                    return f"Error while deleting data from the DataBuffer: {resp.status}"
                else:
                    print(f"Data deleted from DataBuffer")
                    return f"Data deleted from DataBuffer"
                
    @staticmethod
    async def get_data_history(timestamp: int) -> json:
        """get data history from the data buffer

        Args:
           timestamp (int) : timestamp

        Returns:
            json: list of data
        """
        param = {"timestamp": timestamp}
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:23333/sensor/history", params=param) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Error while getting data history from the DataBuffer: {resp.status}"
                    )
                    return f"Error while getting data history from the DataBuffer: {resp.status}"
                else:
                    response = await resp.json()
                    print(f"Data history received from DataBuffer: {response['data']}")
                    return response["data"]
                
    @staticmethod
    async def delete_data_history(timestamp: int) -> str:
        """delete data history from the data buffer

        Args:
            timestamp (int): timestamp

        Returns:
            str: https status code
        """
        param = {"timestamp": timestamp}
        async with aiohttp.ClientSession() as session:
            async with session.delete("http://localhost:23333/sensor/history", params=param) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Error while deleting data history from the DataBuffer: {resp.status}"
                    )
                    return f"Error while deleting data history from the DataBuffer: {resp.status}"
                else:
                    print(f"Data history deleted from DataBuffer")
                    return f"Data history deleted from DataBuffer"