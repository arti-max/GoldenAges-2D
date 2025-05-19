from src.phys.AABB import AABB
from src.customRandom import customRandom
from src.level.tile.Tiles import Tiles

class GrassTile:

    def onTick(level, x: int, y: int, random: customRandom) -> None: # type: ignore
        if (level.isLit(x, y)):
            for _ in range(0, 4, 1):
                targetX: int = x + random.nextInt(3) - 1
                targetY: int = y + random.nextInt(5) - 3

                if (level.getTile(targetX, targetY) == Tiles.DIRT and level.isLit(targetX, targetY)):
                    level.setTile(targetX, targetY, Tiles.GRASS)
        else:
            level.setTile(x, y, Tiles.DIRT)