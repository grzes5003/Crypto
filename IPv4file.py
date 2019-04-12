from RSA import QuasiMD, Extension

class IPv4:
    """ class handling preparation of data and passing it to media """
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

        # TODO optimise
        decoded = [protocol, tos, src_addr, dest_addr, flag, ttl, frame_num, num_of_frames, checksum, data]
        return decoded

    @staticmethod
    def genHADDR():
        return 0b11111111

    def __init__(self, HADDR: int=0b11111111):
        self.ADDRESS = HADDR
        self.QUE = []

    @staticmethod
    def INTTOBIN(i: int) -> bin:
        return bin(i)

    def send_data(self, s_data: str, b_address: bin = None, i_address: int = None):
        """ user socket function to send data to another host"""
        if b_address is None:
            try:
                b_address = IPv4.INTTOBIN(i_address)
            except TypeError as err:
                print("Bad type of i_address: " + str(err.args))
        QUE_DATA = IPv4.ENCAPSULATE(s_data, int, int, int, int)
