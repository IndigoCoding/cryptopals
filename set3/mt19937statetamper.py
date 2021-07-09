# set 3 challenge 23
from mt19937 import MT19937
from time import time

def format32bin(number):
    return "{:032b}".format(number)

def reverseXorRightShift(y, w, l):
    y = format32bin(y)
    result = ''
    for i in range(0, w):
        if i <= l - 1:
            result += y[i]
        elif int(result[i - l]) == 0:
            result += y[i]
        else:
            result += str(1 - int(y[i]))
    return int(result, 2)

def reverseXorLeftShiftMask(y, w, s, b):
    (y, b) = (format32bin(y), format32bin(b))
    result = [None] * w
    for i in range(w - 1, -1, -1):
        if i >= (w - s):
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
        elif int(y[i]) == 0:
            result[i] = str(int(d[i]) & int(result[i - u]))
        else:
            result[i] = str(1 - (int(d[i]) & int(result[i - u])))
    return int("".join(result), 2)

def reverseState(y, tup):
    (w, n, m, r, a, u, d, s, b, t, c, l, f) = tup
    y = reverseXorRightShift(y, w, l)
    y = reverseXorLeftShiftMask(y, w, t, c)
    y = reverseXorLeftShiftMask(y, w, s, b)
    y = reverseXorRightShiftMask(y, w, u, d)
    return y

if __name__ == "__main__":
    mt = MT19937(int(time()))
    attackerMt = MT19937(1)
    tup = (mt.w, mt.n, mt.m, mt.r, mt.a, mt.u, mt.d, mt.s, mt.b, mt.t, mt.c, mt.l, mt.f)
    tamperedState = []
    for i in range(0, 624):
        tamperedState.append(reverseState(mt.extract_number(), tup))
    attackerMt.setState(tamperedState)
    for i in range(20):
        if mt.extract_number() == attackerMt.extract_number():
            print("Correct!")
        else:
            print("Fail!")