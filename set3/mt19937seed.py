# Set 3, challenge 22
from mt19937 import MT19937
from time import time
from random import randint

def guessSeed(num, time):
    for i in range(40, 1000):
        seed = time - i
        mt = MT19937(seed)
        if(mt.extract_number() == num):
            return seed
    return None
    
if __name__ == "__main__":
    now = int(time())
    delta1 = randint(40, 1000)
    seed = now + delta1
    delta2 = randint(40, 1000)
    mt = MT19937(seed)
    nextRand = mt.extract_number()
    outputTime = now + delta1 + delta2
    resultSeed = guessSeed(nextRand, outputTime)
    if(resultSeed == seed):
        print("Correct answer, seed is: " + str(seed))
    else:
        print("Wrong answer")    