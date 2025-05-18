import math
import random
from src.character.Square import Square

BLOCK_PX = 32
HALF_BLOCK_PX = 16

class ZombieModel:
    def __init__(self):
        # Создаем части тела зомби
        self.head = Square(0, 0, 8, 8)  # Голова 8x8
        self.body = Square(8, 8, 4, 12)  # Тело 4x12
        
        # Руки 16x48
        self.rightArm = Square(4, 8, 4, 12)
        self.leftArm = Square(4, 8, 4, 12)
        
        # Ноги 16x48
        self.rightLeg = Square(0, 8, 4, 12)
        self.leftLeg = Square(0, 8, 4, 12)
        
        # Устанавливаем начальные позиции
        self.setup_positions()

    def setup_positions(self):
        # Позиционируем части тела относительно центра
        self.head.setPosition(0, 1.5)  # Голова сверху
        self.head.type = 'head'
        self.body.setPosition(0, 0.6)  # Тело по центру
        
        # Руки по бокам
        self.rightArm.setPosition(0, 0.3)
        self.leftArm.setPosition(0, 0.3)
        
        # Ноги снизу
        self.rightLeg.setPosition(0, -0.5)
        self.leftLeg.setPosition(0, -0.5)

        self.head.setPivot(0.5, 0.8)  # Вращение вокруг нижней части головы (шея)
        self.rightArm.setPivot(0.5, 0.1)  # Вращение вокруг верхней части (плечо)
        self.leftArm.setPivot(0.5, 0.1)
        self.rightLeg.setPivot(0.5, 0.1)  # Вращение вокруг верхней части (бедро)
        self.leftLeg.setPivot(0.5, 0.1)

        self.head.sprite.layer_offset = 10
        self.body.sprite.layer_offset = 5
        self.rightArm.sprite.layer_offset = 10
        self.leftArm.sprite.layer_offset = 4
        self.rightLeg.sprite.layer_offset = 6
        self.leftLeg.sprite.layer_offset = 2

    def add_to_sprite_list(self, sprite_list):
        """Добавляет все спрайты в список для отрисовки"""
        sprite_list.append(self.head)
        sprite_list.append(self.body)
        sprite_list.append(self.rightArm)
        sprite_list.append(self.leftArm)
        sprite_list.append(self.rightLeg)
        sprite_list.append(self.leftLeg)

    def render(self, time: float, entity_x: float, entity_y: float) -> None:
        # Анимация головы
        self.head.xRotation = math.sin(time * 2.0) * 40  # Быстрая анимация

        mirrored = abs(self.head.xRotation) > 90

        # if mirrored:
        #     pass
            #self.head.xRotation = 180 - self.head.xRotation  # Плавность при перевороте

        # Анимация рук: противоположные движения
        arm_angle = math.sin(time * 2.0) * 45  # Увеличенная скорость
        self.rightArm.xRotation = arm_angle
        self.leftArm.xRotation = -arm_angle  # Противоположное движение

        # Анимация ног: противоположные движения
        leg_angle = math.sin(time * 2.0 + math.pi) * 30  # Смещённая фаза
        self.rightLeg.xRotation = leg_angle
        self.leftLeg.xRotation = -leg_angle  # Противоположное движение

        # Отрисовываем все части тела относительно позиции зомби
        # Передаём параметр mirrored, чтобы изменить слои или текстуры при необходимости
        self.head.render(entity_x, entity_y, mirrored=mirrored)
        self.body.render(entity_x, entity_y)

        # Руки и ноги могут зависеть от зеркалирования
        self.rightArm.render(entity_x, entity_y)
        self.leftArm.render(entity_x, entity_y)
        self.rightLeg.render(entity_x, entity_y)
        self.leftLeg.render(entity_x, entity_y)