import random
from typing import Tuple


class Pixel:
    def __init__(self, color: Tuple[int, int, int]):
        self.color = color

    def __str__(self):
        return f"Pixel({self.color})"

    def __repr__(self):
        return self.__str__()


def random_color() -> Tuple[int, int, int]:
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
