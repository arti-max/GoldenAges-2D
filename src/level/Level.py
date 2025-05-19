import math
import random
import pickle
from typing import Dict, List, Tuple

from src.level.Tile import Tile
from src.level.tile.Tiles import Tiles
from src.level.LevelListener import LevelListener
from src.level.PerlinNoiseFilter import PerlinNoiseFilter
from src.phys.AABB import AABB
from src.customRandom import customRandom

class Level:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.blocks: Dict[Tuple[int, int], int] = {}
        self.lightDepths: Dict[int] = {}

        self.random = customRandom()

        self.levelListeners: List[LevelListener] = []

        mapLoaded: bool = self.load()

        if (not mapLoaded):
            self.generateMap()

        self.calcLightDepths(0, self.width)

    
    def save(self) -> None:
        with open('level.dat', 'wb') as dos:
            pickle.dump(self.blocks, dos)

    def load(self) -> None:
        try:
            with open('level.dat', 'rb') as dis:
                self.blocks = pickle.load(dis)
                self.calcLightDepths(0, self.width)

                for listener in self.levelListeners:
                    listener.allChanged()
            
            return True
        except Exception as e:
            return False


    def generateMap(self) -> None:
        firstHeightMap: List[int] = PerlinNoiseFilter(0).read(self.width, self.height)
        secondHeightMap: List[int] = PerlinNoiseFilter(0).read(self.width, self.height)
        cliffMap: List[int] = PerlinNoiseFilter(1).read(self.width, self.height)
        rockMap: List[int] = PerlinNoiseFilter(1).read(self.width, self.height)

        for x in range(0, self.width, 1):
            for y in range(0, self.height, 1):
                idx: int = x + y * self.width

                firstHeightValue: int = firstHeightMap[idx]
                secondHeightValue: int = secondHeightMap[idx]
                cliffValue: int = cliffMap[idx]

                if (cliffValue < 128):
                    secondHeightValue = firstHeightValue

                maxLevelHeight: int = (max(firstHeightValue, secondHeightValue) // 8) + (self.height // 3)
                rockValue: int = rockMap[idx]
                maxRockHeight: int = (rockValue // 8) + (self.height // 3)

                if (maxRockHeight > maxLevelHeight - 2):
                    maxRockHeight = maxLevelHeight - 2
            
                tile_id: int = 0
                if (y == maxLevelHeight):   # GRASS
                    tile_id = 5
                elif (y < maxLevelHeight):  # DIRT
                    tile_id = 4
                
                if (y <= maxRockHeight):    # ROCK
                    tile_id = 2

                self.blocks[(x, y)] = tile_id

    def calcLightDepths(self, minX: int, maxX: int) -> None:
        for x in range(minX, minX + maxX, 1):
            prevDepth: int = self.lightDepths.get(x, 0)

            depth: int = self.height - 1
            while (depth > 0 and (not self.isLightBlocker(x, depth))):
                depth -= 1

            self.lightDepths[x] = depth

            if (prevDepth != depth):
                minTileChangeY: int = min(prevDepth, depth)
                maxTileChangeY: int = max(prevDepth, depth)

                for levelListener in self.levelListeners:
                    levelListener.lightColumnChanged(x, minTileChangeY, maxTileChangeY)

    def onTick(self) -> None:
        totalTiles: int = self.width * self.height

        ticks: int = totalTiles // 100

        for _ in range(0, ticks, 1):
            x = self.random.nextInt(self.width)
            y = self.random.nextInt(self.height)

            tileId: int = self.getTile(x, y)

            if (tileId > 0):
                tile: Tile = Tile(tileId)
                tile.onTick(self, x, y, self.random)

    def getTile(self, x: int, y: int) -> int:
        if (x < 0 or y < 0 or x >= self.width or y >= self.height): return 0

        return self.blocks[(x, y)]
    
    def isLightBlocker(self, x: int, y: int) -> bool:
        tile: Tile = Tile(self.getTile(x, y))
        return tile.id != 0 and tile.blocksLight()
    
    def isTile(self, x: int, y: int) -> bool:
        if (x < 0 or y < 0 or x >= self.width or y >= self.height): return 0

        return self.blocks[(x, y)] != 0
    
    def isSolidTile(self, x: int, y: int) -> bool:
        tile: Tile = Tile(self.getTile(x, y))
        return tile.id != 0 and tile.isSolid()
    
    def isLit(self, x: int, y: int) -> bool:
        return (x < 0 or y < 0 or x >= self.width or y >= self.height or y >= self.lightDepths[x])
        
    def setTile(self, x: int, y: int, id: int) -> bool:
        if (x < 0 or y < 0 or x >= self.width or y >= self.height): return False

        if (id == self.blocks[(x, y)]):
            return False
        
        self.blocks[(x, y)] = id

        self.calcLightDepths(x, 1)

        for levelListener in self.levelListeners:
            levelListener.tileChanged(x, y)

        return True

    def getCubes(self, boundingBox: AABB) -> List[AABB]:
        boundingBoxList: List[AABB] = []

        minX: int = math.floor(boundingBox.minX)
        maxX: int = math.ceil(boundingBox.maxX)
        minY: int = math.floor(boundingBox.minY)
        maxY: int = math.ceil(boundingBox.maxY)

        minX = max(0, minX)
        minY = max(0, minY)

        maxX = min(self.width, maxX)
        maxY = min(self.height, maxY)

        for x in range(minX, maxX, 1):
            for y in range(minY, maxY, 1):
                if (self.isSolidTile(x, y)):
                    tile: Tile = Tile(self.getTile(x, y))

                    block_aabb = tile.getAABB(x, y)
                    if (block_aabb != None):
                        boundingBoxList.append(block_aabb)
        
        return boundingBoxList
    
    def addListener(self, listener: LevelListener) -> None:
        self.levelListeners.append(listener)