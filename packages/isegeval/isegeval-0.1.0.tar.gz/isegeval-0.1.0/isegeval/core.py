from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

import numpy as np
from tqdm import tqdm

from .click.factories import GreatestErrorRegionFactory
from .click.factory import StrategyFactory
from .click.strategy import Click
from .utils import compute_noc, get_iou


class Model(Protocol):
    def predict(self, click: Click) -> np.ndarray:
        pass


class ModelFactory(Protocol):
    def get_model(self, image: np.ndarray) -> Model:
        pass


def evaluate(
    dataset: Sequence[tuple[np.ndarray, np.ndarray]],
    model_factory: ModelFactory,
    threshold: float = 0.9,
    max_clicks: int = 20,
    min_clicks: int = 1,
    strategy_factory: StrategyFactory = GreatestErrorRegionFactory(),
) -> float:
    """Evaluates NoC of the model on the given dataset.

    Args:
        dataset: A sequence of tuple has the pair of images and masks.
        model_factory: A factory for the clicked-based interactive segmentation model.
        threshold: A float value representing an IoU threshold
        to stop an interaction loop.
        max_clicks: A integer value representing a maximum clicks of interaction.
        min_clicks: A integer value representing a minimum clicks of interaction.
        strategy_factory: A factory of the strategy for where to click
        on the given image.

    Returns:
        A float value representing NoC.
    """
    iou_list = []

    for image, ground_truth_mask in tqdm(dataset):
        ious = []

        model = model_factory.get_model(image)
        strategy = strategy_factory.get_strategy(ground_truth_mask)
        prediction_mask = np.zeros_like(ground_truth_mask)

        for i in range(1, max_clicks + 1):
            click = strategy.click(prediction_mask)
            prediction_mask = model.predict(click)

            iou = get_iou(ground_truth_mask, prediction_mask)
            ious.append(iou)

            if iou >= threshold and i >= min_clicks:
                break

        iou_list.append(np.array(ious, dtype=np.float32))

    return compute_noc(iou_list)
