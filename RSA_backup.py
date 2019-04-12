from random import randint

k = 10  # number of characters in one packet


class publKey:
    def __init__(self, n, e):
        self.n = n
        self.e = e


class User:
    # not optimal
    @staticmethod
    def modInverse(a, m):
        a = a % m
        for x in range(1, m):
            if ((a * x) % m == 1):
                return x
        return 1

    @staticmethod
    def nww(a, b):
        if a < b:
            return User.nww(b, a)
        s = a
        while (s % b) != 0:
            s += a
        return s

    @staticmethod
    def extendedEuclides(a, b):
        """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
        x0, x1, y0, y1 = 0, 1, 1, 0
        while a != 0:
            q, b, a = b // a, a, b % a
            y0, y1 = y1, y0 - q * y1
            x0, x1 = x1, x0 - q * x1
        return b, x0, y0

    @staticmethod
    def nwd(a, b):
        while b != 0:
            c = a % b
            a = b
            b = c
        return a

    @staticmethod
    def isPrime(n):
        if (n % 2 == 0) or (n % 3 == 0):
            return False
        i = 5
        while i * i <= n:
            if (n % i == 0) or (n % (i + 2) == 0):
                return False
            i = i + 6
        return True

    def genRSAkey(self):
        """generate public and private RSA key"""

        N = 26**k               # 26 - number of letters in alphabet
        lenN = len(str(N))      # length of N
        lenNum = int(lenN / 2) + 1
        p = randint(10**(lenNum-1), (10**lenNum)-1)
        q = randint(10**(lenNum-1), (10**lenNum)-1)

        while not self.isPrime(p):
            p += 1

        while not self.isPrime(q):
            q += 1

        # e = randint(10**(2*lenNum-1), (10**(2*lenNum))-1)
        e = randint(1, int(User.nww(p-1, q-1)/100))
        # debug
        print("len(p*q) = " + str(len(str(p*q))))
        print("len(e) = " + str(len(str(e))) + " is eq: " + str(e))

        while True:
            # what if e already > than nww
            if self.nwd(e, self.nww(q-1, p-1)) == 1:
                break
            else:
                e += 1

        lowVar = lambda low: [low[0], low[1]] if low[0] > low[1] else [low[1], low[0]]  # return [greater, lower]
        tmp = lowVar([e, User.nww(p-1, q-1)])
        d = User.extendedEuclides(tmp[0], tmp[1])
        # trash
        # d = User.modInverse(e, User.nww(p-1, q-1))

        dSup = lambda de: de[1] if d[1] > 0 else de[2]
        return [[p*q, e], dSup(d)]  # format [[n,e],s]
        # return [[p * q, e], d[1]]  # format [[n,e],s]

    def __init__(self):
        pair = self.genRSAkey()
        self.publKey = publKey(pair[0][0], pair[0][1])
        self.__privKey = pair[1]

    def codeMessage(self, message, publ: publKey):
        return pow(message, publ.e, publ.n)

    def decodeMessage(self, secret):
        return pow(secret, self.__privKey, self.publKey.n)

    def printKeys(self):
        print("public key: " + str(self.publKey.n))
        print("private key: " + str(self.__privKey))
        return [self.publKey, self.__privKey]


def main():
    user1 = User()
    user1.printKeys()


if __name__ == '__main__':
    main()
