from enum import Enum
import arcade

from src.customRandom import customRandom
from src.Textures import Textures

class Tiles:
    GRASS = 5
    ROCK = 2
    DIRT = 4
    COBBLESTONE = 3
    PLANKS = 6

class Tile:
    TEXTURE_COORDS = {
        1: (0, 0),  # GRASS
        2: (1, 0),  # STONE
        3: (0, 1),  # COBBLESTONE
        4: (2, 0),  # DIRT
        5: (3, 0),  # NEW GRASS
        6: (4, 0),  # PLANKS
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

    def onTickGrass(self, level, x: int, y: int, random: customRandom) -> None: # type: ignore
        if (level.isLit(x, y)):
            for i in range(0, 4, 1):
                targetX: int = x + random.nextInt(3) - 1
                targetY: int = y + random.nextInt(5) - 3

                if (level.getTile(targetX, targetY) == Tiles.DIRT and level.isLit(targetX, targetY)):
                    level.setTile(targetX, targetY, Tiles.GRASS)
        else:
            level.setTile(x, y, Tiles.DIRT)

    def onTick(self, level, x: int, y: int, random: customRandom) -> None: # type: ignore
        #print(self.id)
        if (self.id == Tiles.GRASS):
            self.onTickGrass(level, x, y, random)