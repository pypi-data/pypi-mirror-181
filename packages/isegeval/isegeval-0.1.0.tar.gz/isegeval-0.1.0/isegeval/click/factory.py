from abc import ABCMeta, abstractmethod

import numpy as np

from .strategy import Strategy


class StrategyFactory(metaclass=ABCMeta):
    @abstractmethod
    def get_strategy(self, ground_truth_mask: np.ndarray) -> Strategy:
        pass
