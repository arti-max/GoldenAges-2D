from src.level.tile.Tiles import Tiles
from src.phys.AABB import AABB
from src.customRandom import customRandom

class BushTile:


    def onTick(level, x: int, y: int, random: customRandom) -> None:
        tileIdBelow: int = level.getTile(x, y-1)

        if (not level.isLit(x, y) or (tileIdBelow != Tiles.DIRT and tileIdBelow != Tiles.GRASS)):
            level.setTile(x, y, 0)

    def blocksLight() -> bool:
        return False

    def getAABB(x: int, y: int) -> AABB:
        return None
    
    def isSolid() -> bool:
        return False