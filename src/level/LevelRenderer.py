from src.level.LevelListener import LevelListener
from src.level.Chunk import Chunk
from typing import Dict, List
from src.level.Level import Level
from src.Textures import Textures
from src.Player import Player
from src.level.DirtyChunkSorter import DirtyChunkSorter


class LevelRenderer(LevelListener):
    _CHUNK_SIZE: int = 16
    _ATLAS = Textures("res/atlas.png")

    def __init__(self, level: Level):
        level.addListener(self)
        self.level = level

        self.chunkAmountX: int = level.width // LevelRenderer._CHUNK_SIZE
        self.chunkAmountY: int = level.height // LevelRenderer._CHUNK_SIZE

        self.chunks: Dict[Chunk] = {}

        for x in range(0, self.chunkAmountX, 1):
            for y in range(0, self.chunkAmountY, 1):
                minChunkX: int = x * LevelRenderer._CHUNK_SIZE
                minChunkY: int = y * LevelRenderer._CHUNK_SIZE

                maxChunkX: int = (x + 1) * LevelRenderer._CHUNK_SIZE
                maxChunkY: int = (y + 1) * LevelRenderer._CHUNK_SIZE

                maxChunkX = min(level.width, maxChunkX)
                maxChunkY = min(level.height, maxChunkY)

                chunk: Chunk = Chunk(level, LevelRenderer._ATLAS, minChunkX, minChunkY, maxChunkX, maxChunkY)
                self.chunks[(x, y)] = chunk

    def setDirty(self, minX: int, minY: int, maxX: int, maxY: int):

        minX: int = minX // LevelRenderer._CHUNK_SIZE
        minY: int = minY // LevelRenderer._CHUNK_SIZE
        maxX: int = maxX // LevelRenderer._CHUNK_SIZE
        maxY: int = maxY // LevelRenderer._CHUNK_SIZE

        minX = max(minX, 0)
        minY = max(minY, 0)

        maxX = min(maxX, self.chunkAmountX - 1)
        maxY = min(maxY, self.chunkAmountY - 1)


        for x in range(minX, maxX+1, 1):
            for y in range(minY, maxY+1, 1):
                chunk: Chunk = self.chunks[(x, y)]
                chunk.setDirty()

    def getAllDirtyChunks(self) -> List[Chunk]:
        dirty: List[Chunk] = []

        for chunk in self.chunks.values():
            if (chunk.isDirty()):
                dirty.append(chunk)

        return dirty
    
    def updateDirtyChunks(self, player: Player) -> None:
        dirty: List[Chunk] = self.getAllDirtyChunks()

        if (len(dirty) > 0):
            sorter = DirtyChunkSorter(player)
            dirty.sort(key=lambda chunk: chunk.distanceToSqr(player))

            max_updates = min(8, len(dirty))
            for i in range(max_updates):
                dirty[i].rebuildAll()

    def render(self, layer: int, camera_x: float, camera_y: float, screen_width: float, screen_height: float):
        for chunk in self.chunks.values():
            chunk.render(layer, camera_x, camera_y, screen_width, screen_height)

    def lightColumnChanged(self, x: int, minY: int, maxY: int) -> None:
        self.setDirty(x - 1, minY - 1, x + 1, maxY + 1)

    def tileChanged(self, x: int, y: int) -> None:
        self.setDirty(x - 1, y - 1, x + 1, y + 1)
    
    def allChanged(self) -> None:
        self.setDirty(0, 0, self.level.width, self.level.height)