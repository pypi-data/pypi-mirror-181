from abc import ABCMeta, abstractmethod

import numpy as np


class Click:
    def __init__(self, x: int, y: int, is_positive: bool) -> None:
        if x < 0 or y < 0:
            raise ValueError("A coordinate should be positive numbers.")

        self.x = x
        self.y = y
        self.is_positive = is_positive


class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def click(self, segmentation_mask: np.ndarray) -> Click:
        pass
