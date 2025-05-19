import math
import time
import random
import arcade
import arcade.gl
from src.Entity import Entity
from src.level.Level import Level
from src.character.ZombieModel import ZombieModel

class Zombie(Entity):
    def __init__(self, level: Level, x: float, y: float):
        super().__init__(level)

        self.model: ZombieModel = ZombieModel()
        self.setSize(0.6, 1.8)  # Размер хитбокса зомби

        self.speed: float = 0.04
        self.timeOffset: float = random.random() * 1239813.0

        self.mirrored = True if random.random() < 0.04 else False

        self.rotationMotionFactor: float = (random.random() + 1.0) * 0.01
        self.rotation = random.random() * math.pi * 2
        
        # Создаем список спрайтов для отрисовки
        self.parts = []
        self.model.add_to_sprite_list(self.parts)

        self.setPosition(x, y)

    def onTick(self, ai=True) -> None:
        super().onTick()
        
        if (ai):
            # Удаляем зомби, если он упал слишком низко
            if self.y < -100.0:
                self.remove()
                return
            
            # Получаем текущий угол поворота головы
            head_rotation = self.model.head.xRotation
            
            # Определяем зеркалирование и корректируем угол
            if head_rotation > 90:
                self.model.head.xRotation = 180 - head_rotation
                self.mirrored = True
            elif head_rotation < -90:
                self.model.head.xRotation = -180 - head_rotation
                self.mirrored = False
            
            # Корректируем угол движения в зависимости от зеркалирования
            corrected_angle = self.model.head.xRotation if not self.mirrored else 180 - self.model.head.xRotation
            move_angle = math.radians(corrected_angle)
            
            # Вычисляем движение по x на основе угла головы
            move_x = math.sin(move_angle)
            
            # Случайные прыжки
            if self.onGround and random.random() < 0.08:
                self.motionY = 0.5
            
            # Движение
            self.moveRelative(move_x, 0.1 if self.onGround else 0.02)
            
            # Гравитация
            self.motionY -= 0.06
            
            # Обновление позиции
            self.move(self.motionX, self.motionY)
            
            # Замедление
            self.motionX *= 0.91
            self.motionY *= 0.98
            
            # Дополнительное замедление на земле
            if self.onGround:
                self.motionX *= 0.7


    def render(self, partialTicks: float) -> None:
        t: float = time.time_ns() / 1000000000 * 150.0 * self.speed + self.timeOffset

        interpolatedX = (self.prevX + (self.x - self.prevX) * partialTicks) * 32
        interpolatedY = (self.prevY + (self.y - self.prevY) * partialTicks) * 32

        # Анимация перед отрисовкой
        self.model.render(t, interpolatedX, interpolatedY)

        # Сортируем по слоям
        sorted_parts = sorted(self.parts, key=lambda part: part.sprite.layer_offset)

        for part in sorted_parts:
            sprite = part.sprite
            texture = sprite.texture

            x = sprite.center_x
            y = sprite.center_y + 20
            angle = part.xRotation

            width = texture.width * 2.0
            height = texture.height * 2.0

            # Pivot в относительных единицах (например, 0.5, 0.5)
            pivot_x_rel = part.pivot_x
            pivot_y_rel = part.pivot_y
            
            current_texture = None

            if part.type == 'head':
                #self.mirrored = part.mirrored
                #print(self.mirrored)
                current_texture = part._CHAR.get_texture_wh(part.textureOffsetX, part.textureOffsetY, part.width, part.height, flipped=self.mirrored)
            else:
                current_texture = part._CHAR.get_texture_wh(part.textureOffsetX, part.textureOffsetY, part.width, part.height)

            # Пересчитываем left и bottom так, чтобы при повороте объект вращался вокруг pivot
            # Формулы учитывают угол поворота, чтобы компенсировать смещение
            cos_angle = math.cos(math.radians(angle))
            sin_angle = math.sin(math.radians(angle))

            # Центр спрайта (точка, вокруг которой рисуется текстура)
            center_x = x
            center_y = y

            # Смещение pivot относительно центра спрайта
            offset_x = (width * (pivot_x_rel - 0.5))  # pivot=0.5 → нет смещения
            offset_y = (height * (pivot_y_rel - 0.5))

            # После поворота координаты pivot будут смещены
            rotated_offset_x = offset_x * cos_angle - offset_y * sin_angle
            rotated_offset_y = offset_x * sin_angle + offset_y * cos_angle

            # Коррекция позиции, чтобы точка pivot была на месте
            corrected_x = center_x - rotated_offset_x
            corrected_y = center_y - rotated_offset_y

            left = corrected_x - width / 2
            bottom = corrected_y - height / 2

            # Отрисовка с поворотом
            arcade.draw_texture_rect(
                texture=current_texture,
                rect=arcade.LBWH(left, bottom, width, height),
                angle=angle,
                pixelated=True
            )