# set 3 challenge 23
from mt19937 import MT19937

def format32bin(number):
    return "{:032b}".format(number)

def reverseXorRightShift(y, w, l):
    y = format32bin(y)
    result = ''
    for i in range(0, w):
        if i <= l - 1:
            result += y[i]
        elif int(y[i - l]) == 0:
            result += y[i]
        else:
            result += str(1 - int(y[i]))
    return int(result, 2)

def reverseXorLeftShiftMask(y, w, s, b):
    (y, b) = (format32bin(y), format32bin(b))
    result = [None] * w
    for i in range(w - 1, -1, -1):
        if i >= (w - s - 1):
            result[i] = y[i]
        elif int(y[i]) == 0:
            result[i] = str(int(result[s + i]) & int(b[i]))
        else:
            result[i] = str(1 - (int(result[s + i]) & int(b[i])))
    return int("".join(result), 2)

def reverseXorRightShiftMask(y, w, u, d):
    (y, d) = (format32bin(y), format32bin(d))
    result = [None] * w
    for i in range(0, w):
        if i <= u - 1:
            result[i] = y[i]
        elif int(y[i] == 0):
            result[i] = str(int(d[i]) & int(result[i - u]))
        else:
            result[i] = str(1 - (int(d[i]) & int(result[i - u])))
        print(result)
    return int("".join(result), 2)

if __name__ == "__main__":
    (w, n, m, r, a, u, d, s, b, t, c, l, f) = (32, 624, 397, 31, 0x9908B0DF, 11, 0xFFFFFFFF, 7, 0x9D2C5680, 15, 0xEFC60000, 18, 1812433253)
    y = 1919191919
    result = reverseXorRightShiftMask(y, w, u, d)
    print(format32bin(y))
    print(format32bin(result ^ ((result >> u) & d)))