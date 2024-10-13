from abc import ABC, abstractmethod
from typing import List

from pixel import Pixel


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
    def shutdown(self):
        pass

    @abstractmethod
    def set_brightness(self, brightness: int):
        pass


class StubDisplay(Display):
    def display(self):
        print("Displaying pixels")

    def update(self, pixel_array: List[List[Pixel]]):
        print(f"Updating pixels, received {len(pixel_array)} rows")

    def clear(self):
        print("Clearing pixels")

    def shutdown(self):
        print("Shutting down display")

    def set_brightness(self, brightness: int):
        print(f"Setting brightness to {brightness}")
