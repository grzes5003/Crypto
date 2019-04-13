import unittest
from RSAfile import RSA, QuasiMD, Extension
from IPv4file import IPv4
# from layer1 import Layer1

class TestRSA(unittest.TestCase):

    def test_code_decode(self):
        user1 = RSA.RSAGKP(10)
        publickey = user1[0]
        privkey = user1[1]
        message = 1122334455
        secret = RSA.RSAEP(publickey, message)
        # print("len(secret) = " + str(len(str(secret))))
        self.assertEqual(message, RSA.RSADP(privkey, secret))


class TestExtension(unittest.TestCase):

    def test_PAD(self):
        s1 = '10011010101110111010101010111000100110011000'
        a1 = '000010011010101110111010101010111000100110011000'

        self.assertEqual(a1, Extension.PAD(s1, 48))

    def test_ASCIITOBIN(self):
        # s_input = 'abcdefg'
        # s_output = Extension.ASCIITOBIN(s_input)
        # '1100001110001011000111100100110010111001101100111'
        # print(s_output)
        qe = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
        eq = '0100110001101111011100100110010101101101001000000110100101110000011100110111010101101' \
             '1010010000001100100011011110110110001101111011100100010000001110011011010010111010000' \
             '1000000110000101101101011001010111010000101100001000000110001101101111011011100111001' \
             '1011001010110001101110100011001010111010001110101011100100010000001100001011001000110' \
             '1001011100000110100101110011011000110110100101101110011001110010000001100101011011000' \
             '110100101110100'

        self.assertEqual(eq, Extension.ASCIITOBIN(qe))


class TestMD5(unittest.TestCase):

    def test_hash(self):
        s1 = '100010011010101110111010101010111000100110011000'  # 0x89abbaab8998
        s2 = '0b000100100011101110101011101010110011001000010001'  # 0x123babab3211
        i1 = 151370664216984
        i2 = 20047492493841

        # self.assertEqual("1011101001101110", QuasiMD.generate_from_str(s1))
        # self.assertEqual("1100000011100000", QuasiMD.generate_from_str(s2))

        # self.assertEqual("1011101001101110", QuasiMD.generate_from_int(i1))
        # self.assertEqual("1100000011100000", QuasiMD.generate_from_int(i2))

        l1 = []
        for i in range(0b1111111111111111):
            l1.append(QuasiMD.generate_from_int(i))
        from itertools import groupby
        r1 = [len(list(group)) for key, group in groupby(l1)]
        self.assertLessEqual(2, max(r1))


class TestIPv4(unittest.TestCase):

    def test_packet(self):
        ip = IPv4(HADDR=0b00000001)
        segm = 1
        num_of_segm = 1
        src = 0b00000001
        dest = 0b00000010
        flags = 0
        tos = 1
        packet = ip.PACKET('1111', segm, num_of_segm, src, dest, flags, tos)

        # ----------
        # '0b 0100 0001 00000001 00000010 0000 1000 00000001 00000001 10000001000001001111'
        # ----------

        print(packet)
        self.assertEqual('1000000100000100',
                         QuasiMD.generate_from_str('010000010000000100000010000010000000000100000001'))

    def test_encapsulation(self):
        src = 0b00000001
        dest = 0b00000010
        flags = 0
        tos = 1
        qe = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'

        p_list = IPv4.ENCAPSULATE(qe, src, dest, flags, tos)

        print(p_list[2])

        original_ascii = ''
        for p in p_list:
            i = IPv4.DECODEPACKET(p)
            original_ascii += Extension.BINTOASCII(i[9])

        print(original_ascii)

        self.assertEqual(192, len(p_list[0]))


class TestLayer1(unittest.TestCase):

    def test_send_data(self):
        pass