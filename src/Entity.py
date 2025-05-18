import math
import random
from typing import List

from src.phys.AABB import AABB
from src.level.Level import Level

class Entity:

    def __init__(self, level: Level):
        self.level = level

        self.x: float = 0
        self.y: float = 0

        self.prevX: float = 0
        self.prevY: float = 0

        self.motionX: float = 0
        self.motionY: float = 0

        self.boundingBox: AABB = None
        self.boundingBoxWidth: float = 0.6
        self.boundingBoxHeight: float = 1.8

        self.heightOffset: float = 0.0

        self.onGround: bool = False
        self.removed: bool = False

        self.resetPosition()

    def setPosition(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

        width: float = 0.3
        height: float = 0.9

        self.boundingBox = AABB(x - width, y - height, 0, x + width, y + width, 1)

    def resetPosition(self) -> None:
        x: float = random.random() * self.level.width
        y: float = self.level.height + 3

        self.setPosition(x, y)

    def remove(self) -> None:
        self.removed = True

    def setSize(self, width: float, height: float) -> None:
        self.boundingBoxWidth = width
        self.boundingBoxHeight = height

    def onTick(self) -> None:
        self.prevX = self.x
        self.prevY = self.y

    def move(self, x: float, y: float) -> None:
        prevX: float = x
        prevY: float = y

        aABBs: List[AABB] = self.level.getCubes(self.boundingBox.expand(x, y, 0))

        #print(aABBs)

        for abb in aABBs:
            y = abb.clipYCollide(self.boundingBox, y)
        self.boundingBox.move(0.0, y, 0.0)

        for abb in aABBs:
            x = abb.clipXCollide(self.boundingBox, x)
        self.boundingBox.move(x, 0.0, 0.0)

        self.onGround = (prevY != y) and (prevY < 0.0)

        if (prevX != x): self.motionX = 0.0
        if (prevY != y): self.motionY = 0.0

        self.x = (self.boundingBox.minX + self.boundingBox.maxX) / 2.0
        self.y = self.boundingBox.minY + self.heightOffset

    def moveRelative(self, x: float, speed: float) -> None:
        distance = math.sqrt(x * x)
        if (distance < 0.01): return

        normalizedX: float = x / distance

        self.motionX += normalizedX * speed