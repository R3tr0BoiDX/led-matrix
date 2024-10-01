from abc import ABC, abstractmethod
from typing import List, Tuple

from pixel import Pixel


class Effect(ABC):
    @abstractmethod
    def __init__(self, dimensions: Tuple[int, int]):
        pass

    @abstractmethod
    def start(self, buffer: List[List[Pixel]]):
        pass
