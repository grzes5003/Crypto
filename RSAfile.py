from random import randint
import time
import threading

N = 10  # number of characters in one packet


class Medium:
    status: bool

    def __init__(self, stat):
        self.status = stat


class Extension:
    @staticmethod
    def PAD(s: str, i: int) -> str:
        while len(s) < i:
            s = '0' + s
        return s

    @staticmethod
    def ASCIITOBIN(s_data: str) -> str:
        i_list = []
        for s in s_data:
            i_list.append(ord(s))
        s_list = [Extension.PAD(bin(s)[2:], 8) for s in i_list]
        return ''.join(s_list)

    @staticmethod
    def BINTOASCII(b_data: str) -> str:
        ASCII = 8
        b_list = [b_data[i:i+ASCII-1] for i in range(0, len(b_data), ASCII)]
        s_list = [str(chr(int(i, 2))) for i in b_list]
        return ''.join(s_list)


class QuasiMD:
    """
    hash function:
        input: 48 bits
        output: 16 bits
    starting variables:
    OLD
        A = 0x0123
        B = 0x4567
        C = 0x3210
    """
    A = 0x23
    B = 0x45
    C = 0x89
    D = 0xba

    @staticmethod
    def __gen(x: str) -> str:
        l = [x[0:7], x[8:15], x[16:23], x[24:31], x[32:39], x[40:47]]
        i_l = [int(i, 2) for i in l]

        a = QuasiMD.A
        b = QuasiMD.B
        
        c = QuasiMD.C
        d = QuasiMD.D

        a = b + ((a + QuasiMD.__F(b, c, d) + i_l[0] + 0xd7) << 1)
        d = a + ((d + QuasiMD.__F(a, b, c) + i_l[1] + 0xe8) << 2)
        c = d + ((c + QuasiMD.__F(d, c, b) + i_l[2] + 0x24) << 1)
        b = c + ((b + QuasiMD.__F(c, d, a) + i_l[3] + 0xc1) << 2)
        a = b + ((a + QuasiMD.__F(b, c, d) + i_l[4] + 0xf5) << 1)
        d = a + ((d + QuasiMD.__F(a, b, c) + i_l[5] + 0x47) << 2)

        a = b + ((a + QuasiMD.__G(b, c, d) + i_l[0] + 0xf6) << 2)
        d = a + ((d + QuasiMD.__G(a, b, c) + i_l[1] + 0x4a) << 1)
        c = d + ((c + QuasiMD.__G(d, c, b) + i_l[2] + 0x2d) << 2)
        b = c + ((b + QuasiMD.__G(c, d, a) + i_l[3] + 0x3f) << 1)
        a = b + ((a + QuasiMD.__G(b, c, d) + i_l[4] + 0x22) << 2)
        d = a + ((d + QuasiMD.__G(a, b, c) + i_l[5] + 0x7d) << 1)

        a = b + ((a + QuasiMD.__H(b, c, d) + i_l[0] + 0xa5) << 1)
        d = a + ((d + QuasiMD.__H(a, b, c) + i_l[1] + 0xd3) << 2)
        c = d + ((c + QuasiMD.__H(d, c, b) + i_l[2] + 0x3d) << 1)
        b = c + ((b + QuasiMD.__H(c, d, a) + i_l[3] + 0x21) << 2)
        a = b + ((a + QuasiMD.__H(b, c, d) + i_l[4] + 0x6e) << 1)
        d = a + ((d + QuasiMD.__H(a, b, c) + i_l[5] + 0xde) << 2)

        a = b + ((a + QuasiMD.__I(b, c, d) + i_l[0] + 0x8a) << 2)
        d = a + ((d + QuasiMD.__I(a, b, c) + i_l[1] + 0x9e) << 1)
        c = d + ((c + QuasiMD.__I(d, c, b) + i_l[2] + 0xda) << 2)
        b = c + ((b + QuasiMD.__I(c, d, a) + i_l[3] + 0xf3) << 1)
        a = b + ((a + QuasiMD.__I(b, c, d) + i_l[4] + 0xaf) << 2)
        d = a + ((d + QuasiMD.__I(a, b, c) + i_l[5] + 0x19) << 1)

        # TODO: delete
        # a = b | ((a & QuasiMD.__G(a, b) & i_l[2]) << 3)
        # b = a | ((b & QuasiMD.__G(a, b) & i_l[3]) << 4)
        #
        # a = b | ((a & QuasiMD.__H(a, b) & i_l[4]) << 5)
        # b = a | ((b & QuasiMD.__H(a, b) & i_l[5]) << 6)

        final = int(bin(a)[2:] + bin(b)[2:], 2) & int(bin(c)[2:] + bin(d)[2:], 2)
        return bin(final)[2:18]

    @staticmethod
    def generate_from_str(s: str):
        if 'b' in s:
            return QuasiMD.__gen(s[2:])
        return QuasiMD.__gen(s)

    @staticmethod
    def generate_from_int(i: int):
        return QuasiMD.__gen(Extension.PAD(bin(i)[2:], 48))

    @staticmethod
    def __F(x: bin, y: bin, z: bin) -> bin:
        return (x & y) | (~x) & z

    @staticmethod
    def __G(x: bin, y: bin, z: bin) -> bin:
        return (x & z) | (y & (~z))

    @staticmethod
    def __H(x: bin, y: bin, z: bin) -> bin:
        return x & y & z & 1

    @staticmethod
    def __I(x: bin, y: bin, z: bin) -> bin:
        return x & (y | ~z) & 1


class RSA:
    @staticmethod
    def EE(a: int, b: int):
        """ return (x, y, g) such that a*x + b*y = g = gcd(a, b) """
        x, y, u, v = 0, 1, 1, 0
        while a != 0:
            q, r = b // a, b % a
            m, n = x - u * q, y - v * q
            b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
        return x, y, gcd

    @staticmethod
    def GCD(a: int, b: int) -> int:
        while b != 0:
            c = a % b
            a = b
            b = c
        return a

    @staticmethod
    def LCM(a: int, b: int) -> int:
        lcm = (a * b) // RSA.GCD(a, b)
        return lcm

    @staticmethod
    def RSAPRIME(n: int) -> bool:
        if (n % 2 == 0) or (n % 3 == 0):
            return False
        i = 5
        while i * i <= n:
            if (n % i == 0) or (n % (i + 2) == 0):
                return False
            i = i + 6
        return True

    @staticmethod
    def RSAEP(publickey: list, m: int) -> int:  # format: ((n,e), m)
        n, e = publickey[0], publickey[1]
        try:
            if m < 0 or m > n-1:
                raise ValueError('Message representative out of range')
        except ValueError as err:
            print(err.args)

        """ c = m^e mod n """
        # TODO implement pow
        return pow(m, e, n)

    @staticmethod
    def RSADP(K: list, c: int) -> int:  # format: (K, c), K possible form: pair(n,d), another not implemented
        n, d = K[0], K[1]
        try:
            if c < 0 or c > n-1:
                raise ValueError('Ciphertext representative out of range')
        except ValueError as err:
            print(err.args)

        """ m = c^d mod n """
        # TODO implement pow
        return pow(c, d, n)

    @staticmethod
    def RSAGKP(keyLen: int) -> [list, list]:
        # find n = product of u distinct odd primes r_i, i = 2, len(r_i) = keyLen
        # find e = [3, n-1] and GDC(e, \lambda(n)) = 1, where \lambda(n) = LCM(r_1 - 1, r_2 - 1)
        while True:

            p = randint(10 ** (keyLen - 1), (10 ** keyLen) - 1)

            while not RSA.RSAPRIME(p):
                p += 1

            q = randint(10 ** (keyLen - 1), (10 ** keyLen) - 1)

            while not RSA.RSAPRIME(q):
                q += 1

            n = q * p
            ###

            # condition: keyLen is greater than 3
            # e = randint(100, int(q*p/100))
            e = randint(10, int(q * p / 100))

            # debug
            print(q)
            print(p)

            lamb = RSA.LCM(q-1, p-1)

            while RSA.GCD(e, lamb) != 1:
                e += 1

            try:
                if e >= n - 1:
                    raise ValueError('Public key e out of range')
            except ValueError as err:
                print(err.args)
            ###

            d = RSA.EE(e, lamb)[0]

            if d > 0:
                break

        # debug
        print(e)
        print(d)

        return [[n, e], [n, d]]
