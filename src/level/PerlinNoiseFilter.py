import random
from typing import List


class PerlinNoiseFilter:
    FUZZINESS: int = 16

    def __init__(self, octave: int) -> None:
        self.octave = octave

    def read(self, width: int, height: int) -> List[int]:
        # Убедимся, что размеры являются степенями двойки
        width = 1 << (width - 1).bit_length()
        height = 1 << (height - 1).bit_length()
        
        table: List[int] = [0] * (width * height)
        
        # Initial noise generation
        step: int = width >> self.octave
        if step < 1:
            step = 1
            
        for y in range(0, height, step):
            for x in range(0, width, step):
                table[x + y * width] = (random.randint(-128, 127)) * PerlinNoiseFilter.FUZZINESS

        # Noise processing
        while step > 1:
            max_val: int = 256 * (step << self.octave)
            half_step: int = step >> 1

            # First pass - интерполяция между точками
            for y in range(0, height, step):
                for x in range(0, width, step):
                    value: int = table[x + y * width]
                    step_x: int = table[((x + step) % width) + y * width]
                    step_y: int = table[x + ((y + step) % height) * width]
                    step_xy: int = table[((x + step) % width) + ((y + step) % height) * width]
                    
                    # Интерполяция центральной точки
                    mutated: int = ((value + step_x + step_y + step_xy) >> 2) + \
                                  random.randint(0, max_val * 2 - 1) - max_val
                    
                    # Проверяем границы массива
                    center_x = x + half_step
                    center_y = y + half_step
                    if center_x < width and center_y < height:
                        table[center_x + center_y * width] = mutated

            # Second pass - интерполяция между центральными точками
            for y in range(0, height, step):
                for x in range(0, width, step):
                    value: int = table[x + y * width]
                    step_x: int = table[((x + step) % width) + y * width]
                    step_y: int = table[x + ((y + step) % height) * width]
                    
                    # Интерполяция по X
                    center_x = (x + half_step) % width
                    center_y = y
                    if center_x < width and center_y < height:
                        mutated_x = ((value + step_x) >> 1) + \
                                  random.randint(0, max_val * 2 - 1) - max_val
                        table[center_x + center_y * width] = mutated_x
                    
                    # Интерполяция по Y
                    center_x = x
                    center_y = (y + half_step) % height
                    if center_x < width and center_y < height:
                        mutated_y = ((value + step_y) >> 1) + \
                                  random.randint(0, max_val * 2 - 1) - max_val
                        table[center_x + center_y * width] = mutated_y

            step = step >> 1

        # Normalize result
        result: List[int] = [0] * (width * height)
        for y in range(height):
            for x in range(width):
                result[x + y * width] = (table[x + y * width] >> 9) + 128

        return result