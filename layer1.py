from RSAfile import *


class Layer1:
    TICK_RATE = 0.1

    def __init__(self, medium):
        self.medium = medium

    def send_data(self, p_data: str):
        for b in p_data:
            self.medium = int(b)
            time.sleep(Layer1.TICK_RATE)
        return 0
