from RSAfile import *
import threading


class Layer1:
    TICK_RATE = 0.1
    medium: Medium

    def __init__(self, medium):
        self.medium = medium

    def send_data(self, p_data: str):
        for b in p_data:
            if b == '0':
                self.medium.status -= 1
            elif b == '1':
                self.medium.status += 1
            if self.medium != 0 or self.medium != 1:
                time.sleep(Layer1.TICK_RATE*5)
                self.medium.status = 0
                return 1
            time.sleep(Layer1.TICK_RATE)
            print(self.medium)
        # reset medium status after transmission
        self.medium.status = 0
        return 0

    def receive_data(self):
        return self.medium.status
