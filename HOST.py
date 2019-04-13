from IPv4file import IPv4
import layer1

class Host:
    def __init__(self):
        self.ip = IPv4()
        self.s_data = "Some data to be sent"
        self.medium_handler = None

    def connect_to_medium(self, medium):
        """ To connect to particular medium use this method """
        self.medium_handler = medium

    def send_data(self):
        IPv4.send_data(self.s_data, self.medium_handler)
