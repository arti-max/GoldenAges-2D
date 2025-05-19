import math
import time
from typing import List
import arcade
from src.level.LevelRenderer import LevelRenderer
from src.level.Level import Level
from src.level.Chunk import Chunk
from src.Textures import Textures
from src.level.Tile import Tile
from src.level.tile.Tiles import Tiles
from src.Player import Player
from src.Timer import Timer
from src.character.Zombie import Zombie
from src.character.PlayerZombie import PlayerZombie

class Main(arcade.Window):
    MAX_PLACE_DISTANCE = 6

    def __init__(self, width: int, height: int):
        super().__init__(title="2D Craft", width=width, height=height, resizable=True)
        
        self._mouse_mot_x = None
        self._mouse_mot_y = None

        self.level = Level(256, 64)
        self.levelRenderer = LevelRenderer(self.level)
        self.player = Player(self.level)
        self.player_zombie = PlayerZombie(self.level, self.player.x, self.player.y)

        self.zombies: List[Zombie] = []
        
        self.lastTime = time.time()
        self.frames: int = 0

        # Таймер для фиксированных обновлений
        self.timer = Timer(20.0)  # 20 тиков в секунду
        
        # Настройка камеры
        viewport = arcade.Rect(
            left=0,
            right=width,
            bottom=0,
            top=height,
            width=width,
            height=height,
            x=0,
            y=0
        )
        self.camera = arcade.Camera2D(
            viewport=viewport,
            position=(0, 0),
            zoom=1.5
        )
        
        # Управление
        self.left_pressed = False
        self.right_pressed = False
        
        # Выбор блоков
        self.selected_block = Tiles.DIRT  # По умолчанию выбран блок травы
        self.hover_block = None  # Блок под курсором
        self.place_block = None  # Место для размещения блока
        self.blink_timer = 0  # Таймер для мигания
        
        # Создаем спрайт для подсветки размещения блока
        self.place_highlight = arcade.Sprite(
            center_x=0,
            center_y=0,
            image_width=32,
            image_height=32,
            scale=2.0
        )
        # Создаем список спрайтов для отрисовки
        self.place_highlight_list = arcade.SpriteList()
        self.place_highlight_list.append(self.place_highlight)
        
        for _ in range(0, 10, 1):
            zombie: Zombie = Zombie(self.level, 128, 0)
            zombie.resetPosition()
            self.zombies.append(zombie)

        # Получаем текстуру из атласа для выбранного блока
        self.update_place_highlight_texture()


    def _limit_to_reachable_block(self, block_x: int, block_y: int) -> tuple:
        """Находит ближайший доступный блок по линии к курсору"""
        player_x, player_y = self.player.x, self.player.y+1
        
        # Вектор направления
        dx = block_x - player_x
        dy = block_y - player_y
        distance = math.hypot(dx, dy)
        
        # Нормализуем и ограничиваем максимальным расстоянием
        if distance > 0:
            dx /= distance
            dy /= distance
        if distance > self.MAX_PLACE_DISTANCE:
            distance = self.MAX_PLACE_DISTANCE
        
        # Проверяем каждый тайл по линии
        last_valid = None
        steps = int(distance * 4)  # Увеличиваем точность проверки
        for i in range(1, steps + 1):
            t = i / steps
            x = int(player_x + dx * distance * t)
            y = int(player_y + dy * distance * t)
            
            # Запоминаем последний доступный блок
            if self.level.isTile(x, y):
                if not last_valid:  # Первый блок на пути
                    last_valid = (x, y)
                # Проверяем прозрачность
                tile = self.level.getTile(x, y)
                if tile > 0:
                    return (x, y)  # Возвращаем первый непрозрачный блок
            else:
                last_valid = (x, y)  # Запоминаем последнюю доступную позицию
        
        return last_valid if last_valid else (int(player_x), int(player_y))
        
    def update_place_highlight_texture(self):
        # Получаем координаты текстуры из Tile.TEXTURE_COORDS
        if self.selected_block in Tile.TEXTURE_COORDS:
            grid_x, grid_y = Tile.TEXTURE_COORDS[self.selected_block]
            texture = LevelRenderer._ATLAS.get_texture(grid_x, grid_y)
            self.place_highlight.texture = texture

    def update_block_highlight(self):
        if self._mouse_mot_x is None or self._mouse_mot_y is None:
            return
            
        # Учитываем зум камеры (1.5)
        zoom = self.camera.zoom
        
        # Преобразуем координаты мыши с учетом зума
        world_x = (self._mouse_mot_x / zoom + self.camera.position[0] - self.camera.viewport.width // (2 * zoom)) / 32
        world_y = (self._mouse_mot_y / zoom + self.camera.position[1] - self.camera.viewport.height // (2 * zoom)) / 32
        
        block_x = int(world_x)
        block_y = int(world_y)

        # Ограничиваем расстояние
        target_x, target_y = self._limit_to_reachable_block(int(world_x), int(world_y))
    
        if self.level.isTile(target_x, target_y):
            self.hover_block = (target_x, target_y)
            self.place_block = None
        else:
            self.hover_block = None
            # Проверяем, можно ли разместить блок в этой позиции
            if not self.level.isTile(target_x, target_y):
                self.place_block = (target_x, target_y)
            else:
                self.place_block = None
            
    def moveCameraToPlayer(self, partialTicks: int):
        # Вычисляем позицию камеры так, чтобы игрок был в центре
        x: int = self.player.prevX + (self.player.x - self.player.prevX) * partialTicks
        y: int = self.player.prevY + (self.player.y - self.player.prevY) * partialTicks

        screen_center_x = (x * 32)
        screen_center_y = (y * 32) - (self.camera.viewport.height // 2) + (32 * 10)
        
        # Плавное перемещение камеры
        self.camera.position = (screen_center_x, screen_center_y)
        
    def onTick(self):
        self.level.onTick()

        for zombie in self.zombies:
            zombie.onTick()
            if(zombie.removed):
                self.zombies.pop(self.zombies.index(zombie))

        self.player.onTick()
        self.player_zombie.onTick()
            
        # Обработка управления
        if self.left_pressed:
            self.player.move_left()
            self.player_zombie.move_left()
        if self.right_pressed:
            self.player.move_right()
            self.player_zombie.move_right()

    def on_resize(self, width: int, height: int) -> None:
        super().on_resize(width, height)
        viewport = arcade.Rect(
            left=0,
            right=width,
            bottom=0,
            top=height,
            width=width,
            height=height,
            x=0,
            y=0
        )
        self.camera.viewport = viewport
        self.camera.position = (0, 0)

    def on_update(self, delta_time: float):
        self.timer.advance_time()

        for _ in range(self.timer.ticks):
            self.onTick()
            
        self.render(self.timer.partial_ticks)
        #print(time.time(), self.lastTime + 1000)

        self.frames += 1

        while (time.time() >= self.lastTime + 10):
            print(f"{self.frames} fps, {Chunk._updates} chunks updated, {len(self.zombies)} entities")

            Chunk._updates = 0

            self.lastTime += 10
            self.frames = 0

        self.blink_timer = (self.blink_timer + 2) % 30
        
    def render(self, partialTicks: int):
        self.clear(color=(144, 176, 240))

        self.moveCameraToPlayer(partialTicks)
        
        # Активируем камеру
        self.camera.use()

        self.levelRenderer.updateDirtyChunks(self.player)
        
        # Layer 0
        self.levelRenderer.render(0, 
            self.camera.position[0], 
            self.camera.position[1], 
            self.camera.viewport.width, 
            self.camera.viewport.height
        )

        for zombie in self.zombies:
            zombie.render(partialTicks)

        # Layer 1 
        self.levelRenderer.render(1, 
            self.camera.position[0], 
            self.camera.position[1], 
            self.camera.viewport.width, 
            self.camera.viewport.height
        )

        self.update_block_highlight()
        
        # px: int = self.player.prevX + (self.player.x - self.player.prevX) * partialTicks
        # py: int = self.player.prevY + (self.player.y - self.player.prevY) * partialTicks

        # Отрисовка игрока
        # player_x = px * 32
        # player_y = py * 32 + 26
        # player_width = self.player.boundingBoxWidth * 32
        # player_height = self.player.boundingBoxHeight * 30

        self.player_zombie.x = self.player.x
        self.player_zombie.y = self.player.y

        # print(f"PLX: {self.player.x} : {self.player_zombie.x}")
        # print(f"PLY: {self.player.y} : {self.player_zombie.y}")
        
        # pl = arcade.Rect(
        #     left=player_x - player_width/2,
        #     right=player_x + player_width/2,
        #     bottom=player_y - player_height/2,
        #     top=player_y + player_height/2,
        #     width=player_width,
        #     height=player_height,
        #     x=player_x,
        #     y=player_y
        # )
        
        # arcade.draw_rect_filled(
        #     rect=pl,
        #     color=arcade.color.BLUE
        # )

        self.player_zombie.render(self.timer.partial_ticks)
        # self.player_zombie.x = self.player.x
        # self.player_zombie.y = self.player.y
        
        # Отрисовка подсветки блоков
        if self.hover_block:
            block_x = self.hover_block[0] * 32 + 16
            block_y = self.hover_block[1] * 32 + 16
            # Плавное мигание (alpha от 100 до 180)
            alpha = 100 + int(80 * (math.sin(self.blink_timer * 0.2) + 1) / 2)
            highlight = arcade.Rect(
                left=block_x - 16,
                right=block_x + 16,
                bottom=block_y - 16,
                top=block_y + 16,
                width=32,
                height=32,
                x=block_x,
                y=block_y
            )
            arcade.draw_rect_filled(
                rect=highlight,
                color=(255, 255, 255, alpha)
            )
        elif self.place_block:
            # Обновляем позицию спрайта подсветки
            self.place_highlight.center_x = self.place_block[0] * 32 + 16
            self.place_highlight.center_y = self.place_block[1] * 32 + 16
            # Плавное мигание (alpha от 40 до 100)
            alpha = 40 + int(60 * (math.sin(self.blink_timer * 0.2) + 1) / 2)
            self.place_highlight.alpha = alpha
            self.place_highlight_list.draw(filter=arcade.gl.NEAREST)
            
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.player.jump()
            self.player_zombie.jump()
        elif key == arcade.key.R:
            self.player.resetPosition()
            self.player_zombie.x = self.player.x
            self.player_zombie.y = self.player.y
        elif key == arcade.key.G:
            self.zombies.append(Zombie(self.level, self.player.x, self.player.y))
        elif key == arcade.key.ENTER:
            self.level.save()
        # Выбор блоков
        elif key == arcade.key.KEY_1:
            self.selected_block = Tiles.DIRT  # Dirt
            self.update_place_highlight_texture()
        elif key == arcade.key.KEY_2:
            self.selected_block = Tiles.ROCK  # Rock
            self.update_place_highlight_texture()
        elif key == arcade.key.KEY_3:
            self.selected_block = Tiles.COBBLESTONE  # Cobble
            self.update_place_highlight_texture()
        elif key == arcade.key.KEY_4:
            self.selected_block = Tiles.PLANKS  # Planks
            self.update_place_highlight_texture()
        elif key == arcade.key.KEY_6:
            self.selected_block = Tiles.BUSH    # Bush
            self.update_place_highlight_texture()
            
    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.left_pressed = False
            if not self.right_pressed:
                self.player_zombie.stop()
        elif key == arcade.key.D:
            self.right_pressed = False
            if not self.left_pressed:
                self.player_zombie.stop()
            
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # Сохраняем текущие координаты мыши
        self._mouse_mot_x = x
        self._mouse_mot_y = y
        self.update_block_highlight()
            
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT and self.place_block:
            self.level.setTile(self.place_block[0], self.place_block[1], self.selected_block)
        elif button == arcade.MOUSE_BUTTON_RIGHT and self.hover_block:
            self.level.setTile(self.hover_block[0], self.hover_block[1], 0)

if __name__ == "__main__":
    g = Main(1080, 720)
    arcade.run()