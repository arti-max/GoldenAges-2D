import math
import arcade
from src.Textures import Textures

class Square:
    _CHAR = Textures("res/char.png")

    def __init__(self, textureOffsetX: int, textureOffsetY: int, width: int = 1, height: int = 1, layer: int = 0):
        self.textureOffsetX: int = textureOffsetX
        self.textureOffsetY: int = textureOffsetY
        self.width: int = width
        self.height: int = height

        self.mirrored = False
        self.type = 'none'

        self.layer_offset = layer

        self.pivot_x = 0.5  # 0.5 = центр (по умолчанию)
        self.pivot_y = 0.5  # 0.5 = центр (по умолчанию)

        self.x: float = 0
        self.y: float = 0
        self.xRotation: float = 0  # Вращение вверх-вниз
        
        # Создаем спрайт для отрисовки
        self.sprite = arcade.Sprite(
            center_x=0,
            center_y=0,
            image_width=width,
            image_height=height,
            scale=2.5
        )

        # Получаем текстуру из атласа
        self.update_texture()

    def setPivot(self, x_ratio: float, y_ratio: float):
        """Устанавливает точку вращения относительно размеров спрайта
           (0,0) - левый нижний угол, (1,1) - правый верхний"""
        self.pivot_x = x_ratio
        self.pivot_y = y_ratio

    def update_texture(self):
        """Обновляет текстуру спрайта"""
        texture = Square._CHAR.get_texture_wh(
            self.textureOffsetX,
            self.textureOffsetY,
            self.width,
            self.height
        )
        self.sprite.texture = texture

    def setTextureOffset(self, textureOffsetX: int, textureOffsetY: int) -> None:
        self.textureOffsetX = textureOffsetX
        self.textureOffsetY = textureOffsetY
        self.update_texture()

    def setPosition(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def get_pivot_position(self):
        """Возвращает координаты точки вращения (pivot) в абсолютных координатах"""
        texture = self.sprite.texture
        width = texture.width * self.sprite.scale
        height = texture.height * self.sprite.scale

        pivot_x_abs = self.sprite.center_x - width * self.pivot_x
        pivot_y_abs = self.sprite.center_y - height * self.pivot_y

        return pivot_x_abs, pivot_y_abs


    def render(self, entity_x: float, entity_y: float, mirrored: bool = False) -> None:
        # Переводим координаты в пиксели и добавляем смещение части тела
        x: float = entity_x + self.x * 32
        y: float = entity_y + self.y * 32

        self.sprite.center_x = x
        self.sprite.center_y = y

        # Сохраняем угол поворота
        self.sprite.angle = self.xRotation

        # Можно сохранить mirrored как свойство спрайта, если нужно менять текстуру
        self.mirrored = mirrored
        