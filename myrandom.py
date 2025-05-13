import random

def use(min, max):
    rnd = random.SystemRandom()
    return rnd.choice(range(min, max))

def choice(arr):
    rnd = random.SystemRandom()
    return rnd.choice(arr)

def randint(min, max):
    rnd = random.SystemRandom()
    return rnd.randint(min, max)