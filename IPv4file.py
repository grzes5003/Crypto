# TODO potential mistake
# from RSAfile import QuasiMD, Extension
from layer1 import *
import threading


class IPv4(threading.Thread):
    """ class handling preparation of data and passing it to layer1
        class handles also receiving data from layer1
    """
    SIZE = 128  # number of bits in payload
    PROTOCOL = '0100'

    # TODO delete method
    @staticmethod
    def PAD(s: str, i: int) -> str:
        while len(s) < i:
            s = '0' + s
        return s

    @staticmethod
    def ENCAPSULATE(s_data: str, i_source_address: int, i_dest_address: int, i_flags: int, i_tos: int) -> list:
        b_data = Extension.ASCIITOBIN(s_data)
        # TODO probably does not work
        b_list = [b_data[i:i+IPv4.SIZE] for i in range(0, len(b_data), IPv4.SIZE)]

        # TODO add some sort of 'end of data' signal
        while len(b_list[-1]) < IPv4.SIZE:
            b_list[-1] += '0'

        p_list = []
        segm = 0
        num_of_segm = len(b_list) - 1
        for i in b_list:
            p_list.append(IPv4.PACKET(i, segm, num_of_segm, i_source_address, i_dest_address, i_flags, i_tos))
            segm += 1
        return p_list

    @staticmethod
    def PACKET(b_data: str, i_segm: int, i_num_of_segm: int, i_src_address: int, i_dest_address: int,
               i_flags: int, i_tos: int) -> bin:
        """
        Header

         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        | Fixed |  ToS  |  Src Address  |  Dest Address | Flags |  TTL  |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |  Frame Number | Num of Frames |        Header Checksum        |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

        Fixed: 4 bits
         start of packet, value: 0b0100

        Tos: 4 bits
         type of service (containing protocol type as well)
         - currently only 0b0001

        """
        # TODO check all types

        frame = IPv4.PROTOCOL

        # TODO test PAD
        s_tos = Extension.PAD(str(bin(i_tos))[2:], 4)
        frame += s_tos
        # ------------------
        # add src and dest to frame
        # ------------------
        s_src_addr = Extension.PAD(bin(i_src_address)[2:], 8)
        s_des_addr = Extension.PAD(bin(i_dest_address)[2:], 8)
        frame += s_src_addr
        frame += s_des_addr
        # ------------------
        # add flag
        # ------------------
        # TODO add flags usage
        frame += '0000'
        # ------------------
        # add TTL
        # ------------------
        frame += '1000'
        # ------------------
        # add segment number
        # ------------------
        s_segm = Extension.PAD(str(bin(i_segm))[2:], 8)
        frame += s_segm
        # ------------------
        # add numb of segments
        # ------------------
        s_num_of_segm = Extension.PAD(str(bin(i_num_of_segm))[2:], 8)
        frame += s_num_of_segm
        # ------------------
        # add header checksum
        # ------------------
        s_check_sum = QuasiMD.generate_from_str(frame)
        frame += s_check_sum
        # ------------------
        # add data
        # ------------------
        frame += b_data

        return frame

    @staticmethod
    def DECODEPACKET(p_data: str):
        """
        Header

            0                   1                   2                   3
            0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            | Fixed |  ToS  |  Src Address  |  Dest Address | Flags |  TTL  |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |  Frame Number | Num of Frames |        Header Checksum        |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Fixed: 4 bits
                start of packet, value: 0b0100

            Tos: 4 bits
                type of service (containing protocol type as well)
                - currently only 0b0001

        """
        # TODO add error handler
        protocol = p_data[0:4]
        tos = p_data[4:8]
        src_addr = p_data[8:16]
        dest_addr = p_data[16:24]
        flag = p_data[24:28]
        ttl = p_data[28:32]
        frame_num = p_data[32:40]
        num_of_frames = p_data[40:48]
        checksum = p_data[48:65]
        data = p_data[65:192]
        HEADER = p_data[0:65]

        # TODO optimise
        decoded = {"protocol": protocol,
                   "tos": tos,
                   "src_addr": src_addr,
                   "dest_addr": dest_addr,
                   "flag": flag,
                   "ttl": ttl,
                   "frame_num": frame_num,
                   "num_of_frames": num_of_frames,
                   "checksum": checksum,
                   "data": data,
                   "HEADER": HEADER
                   }
        return decoded

    @staticmethod
    def genHADDR():
        return 0b11111111

    def __init__(self, listen_status, HADDR: int=0b11111111):
        self.ADDRESS = HADDR
        self.QUE = []
        self.listen_status = listen_status
        self.listener_handler: Listener = None
        self.layer_handler = None
        threading.Thread.__init__(self)

    @staticmethod
    def INTTOBIN(i: int) -> bin:
        return bin(i)

    def send_data(self, s_data: str, layer_handler, b_address: str = None, i_address: int = None):
        """ user socket function to send data to another host"""

        # user must be connected
        if self.listener_handler is None:
            # not connected
            return 1

        # TODO listen_status not needed
        self.listen_status = False
        self.listener_handler.change_listen_status(self.listen_status)

        if b_address is None:
            try:
                b_address = IPv4.INTTOBIN(i_address)
            except TypeError as err:
                print("Bad type of i_address: " + str(err.args))
        # TODO remove default values
        src, dest, flags, tos = 1, 2, 0, 1

        QUE_DATA = IPv4.ENCAPSULATE(s_data, src, dest, flags, tos)

        # TODO real error handler
        for P in QUE_DATA:
            if layer_handler.send_data(P) != 0:
                print('Error occurred')

    def connect_to_medium(self, medium: Medium):
        self.layer_handler = Layer1(medium)
        self.listener_handler = Listener(self.layer_handler)
        self.listener_handler.start()

    # threading methods
    def get_data_from_listen(self):
        pass

    def run(self):
        while True:
            if self.listen_status:
                self.get_data_from_listen()
                time.sleep(0.5)


class Listener(threading.Thread):
    BUFFOR_LIMIT = 1024
    layer_handler: Layer1
    ascii_data: str

    def __init__(self, layer_handler):
        self.listen_status = True
        self.buffor = ''
        self.layer_handler = layer_handler
        threading.Thread.__init__(self)

    def change_listen_status(self, status):
        self.listen_status = status

    def run(self):
            while True:
                # if IPv4 wants to receive data, listen and add it to buffor
                if self.listen_status:
                    self.buffor += self.layer_handler.receive_data()
                    if IPv4.PROTOCOL in self.buffor:
                        # if PROTOCOL (0100) substring in buffor
                        s_tmp = self.buffor[self.buffor.find(IPv4.PROTOCOL):]
                        # if its whole packet length
                        if len(s_tmp) >= 192:
                            self.decode(s_tmp)

                    # analise buffor

    def decode(self, p_data):
        # TODO add error handling
        if len(p_data) != 192:
            # bad frame length
            return 1

        frame = IPv4.DECODEPACKET(p_data)

        if frame["checksum"] != QuasiMD.generate_from_str(frame["HEADER"]):
            # TODO throw frame away
            return 1
        self.ascii_data += Extension.BINTOASCII(frame["data"])

    def return_ascii_data(self):
        data_tmp = self.ascii_data
        self.ascii_data = ''
        return data_tmp
