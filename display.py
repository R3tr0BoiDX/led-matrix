from abc import ABC, abstractmethod
from typing import List

from pixel import Pixel

# todo: use values from config
PIXEL_WIDTH = 32


class Display(ABC):
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def update(self, pixel_array: List[List[Pixel]]):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def exit(self):
        pass
