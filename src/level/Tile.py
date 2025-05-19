from enum import Enum
import arcade

from src.level.tile.GrassTile import GrassTile
from src.level.tile.BushTile import BushTile
from src.phys.AABB import AABB
from src.customRandom import customRandom
from src.Textures import Textures
from src.level.tile.Tiles import Tiles

class Tile:
    TEXTURE_COORDS = {
        1: (0, 0),  # GRASS
        2: (1, 0),  # STONE
        3: (0, 1),  # COBBLESTONE
        4: (2, 0),  # DIRT
        5: (3, 0),  # NEW GRASS
        6: (4, 0),  # PLANKS
        7: (15, 0), # BUSH
    }
    
    def __init__(self, id: int):
        self.id = id
        self.sprite = None

    def create_sprite(self, atlas):
        """Создаем спрайт с правильной инициализацией"""
        if self.id in self.TEXTURE_COORDS:
            grid_x, grid_y = self.TEXTURE_COORDS[self.id]
            texture = atlas.get_texture(grid_x, grid_y)
            self.sprite = arcade.Sprite(
                center_x=0,
                center_y=0,
                image_width=16,
                image_height=16,
                scale=2.0
            )
            self.sprite.texture = texture

    def onTick(self, level, x: int, y: int, random: customRandom) -> None: # type: ignore
        #print(self.id)
        if (self.id == Tiles.GRASS):
            GrassTile.onTick(level, x, y, random)
        elif (self.id == Tiles.BUSH):
            BushTile.onTick(level, x, y, random)


    def getAABB(self, x: int, y: int) -> AABB:
        if (self.id == Tiles.BUSH):
            return BushTile.getAABB(x, y)
        else:
            return AABB(x, y, 0, x+1, y+1, 1)
        
    def blocksLight(self) -> bool:
        if (self.id == Tiles.BUSH):
            return BushTile.blocksLight()
        else:
            return True
        
    def isSolid(self) -> bool:
        if (self.id == Tiles.BUSH):
            return BushTile.isSolid()
        else:
            return True
        
    