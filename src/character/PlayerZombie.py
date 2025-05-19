# src/character/PlayerZombie.py

import math
import time

import arcade
from src.character.Zombie import Zombie

class PlayerZombie(Zombie):
    def __init__(self, level, x, y):
        super().__init__(level, x, y)
        self.setSize(0.6, 1.8)
        self.is_walking = False
        self.last_direction = 1  # 1 - вправо, -1 - влево
        self.gravity = 0.06
        self.jumpSpeed = 0.58

    def onTick(self):
        super().onTick(ai=False)

        # Применяем гравитацию
        self.motionY -= self.gravity
        
        # Обновляем позицию
        self.move(self.motionX, self.motionY)
        
        # Замедление по горизонтали
        self.motionX *= 0.86
        self.motionY *= 0.98

        if (self.onGround):
            self.motionY = 0
            self.motionX *= 0.95

    def move_left(self):
        self.moveRelative(-1, self.speed)
        self.is_walking = True
        self.last_direction = -1

    def move_right(self):
        self.moveRelative(1, self.speed)
        self.is_walking = True
        self.last_direction = 1

    def stop(self):
        self.motionX = 0
        self.is_walking = False
    
    def jump(self):
        if self.onGround:
            self.motionY = self.jumpSpeed
            self.onGround = False

    def render(self, partialTicks: float):
        # Управляем анимацией: если стоит - не анимируем, если идёт - анимируем
        t = time.time_ns() / 1000000000 * 150.0 * self.speed + self.timeOffset if self.is_walking else 0
        interpolatedX = (self.prevX + (self.x - self.prevX) * partialTicks) * 32
        interpolatedY = (self.prevY + (self.y - self.prevY) * partialTicks) * 32

        # Устанавливаем направление головы и зеркалирование
        self.model.head.xRotation = 0 if not self.is_walking else (40 if self.last_direction > 0 else -40)
        self.mirrored = self.last_direction < 0

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
