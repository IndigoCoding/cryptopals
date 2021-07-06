from time import time
import random
# init mt19937-32bit constant
(w, n, m, r, a, u, d, s, b, t, c, l, f) = (32, 624, 397, 31, 0x9908B0DF, 11, 0xFFFFFFFF, 7, 0x9D2C5680, 15, 0xEFC60000, 18, 1812433253)

def extractWBits(num, w):
    binary = bin(num)[2:]
    start = (len(binary) - w) if len(binary) >= w else 0
    wBitSubStr = binary[start :]
    return (int(wBitSubStr, 2))

# init global variable
MT = [None] * n
index = n + 1
lower_mask = (1 << r) - 1 # r of 1's
upper_mask = extractWBits(~lower_mask, w)

def seed_mt(seed):
    global index, MT
    index = n
    MT[0] = seed
    for i in range(1, n):
        MT[i] = extractWBits(f * (MT[i - 1] ^ (MT[i - 1] >> (w - 2))) + i, w)

def extract_number():
    global index
    if(index >= n):
        if(index > n):
            raise Exception("Generator was never seeded")
        twist()
    y = MT[index]
    y = y ^ ((y >> u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)
    index += 1
    return extractWBits(y, w)

def twist():
    global MT, index
    for i in range(0, n):
        x = (MT[i] & upper_mask) + (MT[(i + 1) % n] & lower_mask)
        xA = x >> 1
        if x % 2 != 0: # lowest bit = 1
            xA ^= a
        MT[i] = MT[(i + m) % n] ^ xA
    index = 0

if __name__ == '__main__':
    # seed_mt(int(time()))
    seed_mt(123)
    zzz = list()
    for i in range(0, 10):
        zzz.append(extract_number())
    print(zzz)