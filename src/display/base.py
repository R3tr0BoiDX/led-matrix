from abc import ABC, abstractmethod
from typing import List

from src import log
from src.pixel import Pixel


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

    logger = log.get_logger(__name__)

    def display(self):
        self.logger.debug("Displaying pixels")

    def update(self, pixel_array: List[List[Pixel]]):
        self.logger.debug("Updating pixels, received %s rows", len(pixel_array))

    def clear(self):
        self.logger.debug("Clearing pixels")

    def shutdown(self):
        self.logger.debug("Shutting down display")

    def set_brightness(self, brightness: int):
        self.logger.debug("Setting brightness to %s", brightness)
