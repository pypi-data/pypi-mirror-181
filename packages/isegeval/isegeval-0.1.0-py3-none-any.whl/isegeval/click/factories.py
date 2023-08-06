import numpy as np

from .factory import StrategyFactory
from .strategies import GreatestErrorRegion


class GreatestErrorRegionFactory(StrategyFactory):
    def __init__(self, ignore_label: int = -1):
        self.ignore_label = ignore_label

    def get_strategy(self, ground_truth_mask: np.ndarray) -> GreatestErrorRegion:
        return GreatestErrorRegion(ground_truth_mask, self.ignore_label)
