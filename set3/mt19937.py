# Set 3, challenge 21
class MT19937:
    def __init__(self, seed):
        # init mt19937-32bit constant
        (self.w, self.n, self.m, self.r, self.a, self.u, self.d, self.s, self.b, self.t, self.c, self.l, self.f) = (32, 624, 397, 31, 0x9908B0DF, 11, 0xFFFFFFFF, 7, 0x9D2C5680, 15, 0xEFC60000, 18, 1812433253)

        # init global variable
        self.MT = [None] * self.n
        self.index = self.n + 1
        self.lower_mask = (1 << self.r) - 1 # r of 1's
        self.upper_mask = self.extractWBits(~self.lower_mask, self.w)
        self.seed_mt(seed)

    def extractWBits(self, num, w):
            binary = bin(num)[2:]
            start = (len(binary) - w) if len(binary) >= w else 0
            wBitSubStr = binary[start :]
            return (int(wBitSubStr, 2))

    def seed_mt(self, seed):
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = self.extractWBits(self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i, self.w)

    def extract_number(self):
        if(self.index >= self.n):
            if(self.index > self.n):
                raise Exception("Generator was never seeded")
            self.twist()
        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        self.index += 1
        return self.extractWBits(y, self.w)

    def twist(self):
        for i in range(0, self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0: # lowest bit = 1
                xA ^= self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0

if __name__ == '__main__':
    mt = MT19937(123)
    zzz = list()
    for i in range(0, 10):
        zzz.append(mt.extract_number())
    print(zzz)