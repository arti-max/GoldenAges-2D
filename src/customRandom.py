import math
import random

class customRandom:
    def __init__(self):
        pass

    def nextInt(self, max: int) -> int:
        return math.floor(random.random() * max)