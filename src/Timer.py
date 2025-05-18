import time

class Timer:
    NS_PER_SECOND = 1_000_000_000
    MAX_NS_PER_UPDATE = 1_000_000_000
    MAX_TICKS_PER_UPDATE = 100

    def __init__(self, ticks_per_second: float):
        self.ticks_per_second = ticks_per_second
        self.last_time = time.time_ns()
        self.time_scale = 1.0
        self.fps = 0.0
        self.passed_time = 0.0
        self.ticks = 0
        self.partial_ticks = 0.0

    def advance_time(self):
        now = time.time_ns()
        passed_ns = now - self.last_time

        # Сохраняем время этого обновления
        self.last_time = now

        # Максимум и минимум
        passed_ns = max(0, passed_ns)
        passed_ns = min(self.MAX_NS_PER_UPDATE, passed_ns)

        # Вычисляем fps
        self.fps = float(self.NS_PER_SECOND / passed_ns)

        # Вычисляем прошедшее время и тики
        self.passed_time += passed_ns * self.time_scale * self.ticks_per_second / self.NS_PER_SECOND
        self.ticks = int(self.passed_time)

        # Максимум тиков за обновление
        self.ticks = min(self.MAX_TICKS_PER_UPDATE, self.ticks)

        # Вычисляем остаток текущего тика
        self.passed_time -= self.ticks
        self.partial_ticks = self.passed_time