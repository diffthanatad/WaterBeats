import numpy as np

class edge_data_processor:
    # * This class is used to process the data from the sensor (how to process the data is not decided yet)
    def compute_avg(self,data: list()) -> float:
        return np.mean(data)

    def compute_min(self,data: list()) -> float:
        return np.min(data)
    
    def compute_max(self,data: list()) -> float:
        return np.max(data)

