import arcade
from src.Textures import Textures
from src.level.Tile import Tile
from src.phys.AABB import AABB
from src.level.Level import Level
from src.Player import Player

from pyglet.gl import GL_NEAREST
from pyglet.gl import GL_LINEAR


class Chunk:

    _updates: int = 0
    _totalUpdates: int = 0

    def __init__(self, level: Level, atlas: Textures, minX: int, minY: int, maxX: int, maxY: int):
        self.level = level
        self.atlas = atlas

        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY

        self.x: float = (minX + maxX) / 2.0
        self.y: float = (minY + maxY) / 2.0

        self.dirty = True
        self.visible = True

        self.boundingBox: AABB = AABB(minX, minY, 0, maxX, maxY, 1)

        self.tile_sprites_0 = arcade.SpriteList()
        self.tile_sprites_1 = arcade.SpriteList()

        self.rebuildAll()

    def isVisible(self, camera_x: float, camera_y: float, screen_width: float, screen_height: float) -> bool:
        # Добавляем буферную зону (90% от размера экрана)
        buffer = min(screen_width, screen_height) * 0.9
        
        # Проверяем, находится ли чанк в поле зрения камеры с учетом буфера
        chunk_left = self.minX * 32
        chunk_right = self.maxX * 32
        chunk_bottom = self.minY * 32
        chunk_top = self.maxY * 32

        screen_left = camera_x - buffer
        screen_right = camera_x + screen_width + buffer
        screen_bottom = camera_y - buffer
        screen_top = camera_y + screen_height + buffer

        return not (chunk_right < screen_left or 
                   chunk_left > screen_right or 
                   chunk_top < screen_bottom or 
                   chunk_bottom > screen_top)

    def rebuild(self, layer: int):
        if not self.dirty:
            return

        Chunk._updates += 1
        self.dirty = False
        if (layer == 0):
            self.tile_sprites_0.clear()
        elif (layer == 1):
            self.tile_sprites_1.clear()

        tiles: int = 0

        for x in range(self.minX, self.maxX, 1):
            for y in range(self.minY, self.maxY, 1):
                tileId: int = self.level.getTile(x, y)
                if (tileId > 0):
                    tile = Tile(tileId)
                    tile.create_sprite(self.atlas)
                    if (tile.sprite):
                        tile.sprite.center_x = x * 32 + 16
                        tile.sprite.center_y = y * 32 + 16
                        
                        is_lit = self.level.isLit(x, y)
                        
                        # Слой 0 - только светлые блоки
                        if layer == 0 and is_lit:
                            shadow = arcade.SpriteSolidColor(
                                width=32,
                                height=32,
                                color=(0, 0, 0, 65)
                            )

                            shadow.center_x = tile.sprite.center_x
                            shadow.center_y = tile.sprite.center_y
                            
                            self.tile_sprites_0.append(tile.sprite)
                            self.tile_sprites_0.append(shadow)
                            tiles += 1
                        # Слой 1 - только темные блоки с наложением черного
                        elif layer == 1 and not is_lit:
                            # Создаем черный прямоугольник для затемнения
                            shadow = arcade.SpriteSolidColor(
                                width=32,
                                height=32,
                                color=(0, 0, 0, 140)
                            )
                            shadow.center_x = tile.sprite.center_x
                            shadow.center_y = tile.sprite.center_y
                            
                            self.tile_sprites_1.append(tile.sprite)
                            self.tile_sprites_1.append(shadow)
                            tiles += 1

        if (tiles > 0):
            Chunk._totalUpdates += 1

    def isDirty(self):
        return self.dirty
    
    def setDirty(self):
        if (not self.dirty):
            self.dirty = True

    def rebuildAll(self):
        self.rebuild(0)
        self.dirty = True
        self.rebuild(1)

    def render(self, layer: int, camera_x: float, camera_y: float, screen_width: float, screen_height: float):
        if not self.isVisible(camera_x, camera_y, screen_width, screen_height):
            return
        
        self.rebuild(layer)


        if (layer == 0):
            self.tile_sprites_0.draw(filter=GL_NEAREST)
        elif (layer == 1):
            self.tile_sprites_1.draw(filter=GL_NEAREST)

    def distanceToSqr(self, player: Player) -> float:
        distanceX: float = player.x - self.x
        distanceY: float = player.y - self.y

        return distanceX * distanceX + distanceY * distanceY