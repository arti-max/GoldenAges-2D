from src.Entity import Entity
from src.level.Level import Level

class Player(Entity):
    def __init__(self, level: Level):
        super().__init__(level)
        self.setSize(0.6, 1.8)  # Размер хитбокса игрока
        self.resetPosition()
        
        # Физические параметры
        self.speed = 0.04
        self.jumpSpeed = 0.58
        self.gravity = 0.06
        
    def onTick(self):
        super().onTick()

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
        
    def move_right(self):
        self.moveRelative(1, self.speed)
        
    def jump(self):
        if self.onGround:
            self.motionY = self.jumpSpeed
            self.onGround = False