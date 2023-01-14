import math
import random
import time


class Simulator:
    def __init__(self):
        self.x = 0

    def start(self) -> None:
        pass

    def generate_data(self):
        self.x += 1
        value = 2 * math.sin(self.x) + 3
        value += 3 * random.random()
        return value

    def send_data(self):
        pass

if __name__ == '__main__':
    s = Simulator()
    while(True):
        time.sleep(1)
        print(s.x, s.generate_data())