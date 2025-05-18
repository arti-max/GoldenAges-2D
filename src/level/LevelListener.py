from abc import ABC, abstractmethod


class LevelListener(ABC):
    
    @abstractmethod
    def lightColumnChanged(self, x: int, minY: int, maxY: int) -> None:
        pass
    
    @abstractmethod
    def tileChanged(self, x: int, y: int) -> None:
        pass
    
    @abstractmethod
    def allChanged(self) -> None:
        pass