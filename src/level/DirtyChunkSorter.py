import arcade
from src.Player import Player
from src.level.Chunk import Chunk

class DirtyChunkSorter:
    def __init__(self, player: Player):
        self.player = player
        
    def compare(self, chunk1: Chunk, chunk2: Chunk) -> int:
        # Сравниваем расстояния от чанков до игрока
        dist1 = chunk1.distanceToSqr(self.player)
        dist2 = chunk2.distanceToSqr(self.player)
        
        if dist1 < dist2:
            return -1
        elif dist1 > dist2:
            return 1
        return 0

    def is_in_viewport(self, chunk: Chunk) -> bool:
        # Получаем границы вьюпорта камеры
        viewport = self.camera.viewport
        camera_left = viewport[0]
        camera_right = viewport[0] + viewport[2]
        camera_bottom = viewport[1]
        camera_top = viewport[1] + viewport[3]
        
        # Проверка пересечения прямоугольников
        return not (chunk.maxX < camera_left or 
                   chunk.minX > camera_right or
                   chunk.maxY < camera_bottom or 
                   chunk.minY > camera_top)