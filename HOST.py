from IPv4file import IPv4
from layer1 import Layer1
from RSAfile import Status

class Host:
    def __init__(self):
        self.listen_status = Status(True)
        self.ip = IPv4(self.listen_status)
        self.s_data = "Some data to be sent"
        self.medium_handler = None

        # thread listener

    def connect_to_medium(self, medium):
        """ To connect to particular medium use this method
            connection through IPv4 class
        """
        # self.medium_handler = Layer1(medium)
        self.ip.connect_to_medium(medium)

    def send_data(self):
        IPv4.send_data(s_data=self.s_data, layer_handler=self.medium_handler)
