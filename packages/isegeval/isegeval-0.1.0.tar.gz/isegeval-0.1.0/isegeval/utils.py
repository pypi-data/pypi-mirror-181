from __future__ import annotations

from typing import cast

import numpy as np


def get_iou(
    ground_truth: np.ndarray, prediction: np.ndarray, ignore_label: int = -1
) -> float:
    """Computes intersection over union (IoU).

    Args:
        ground_truth: A float array representing a ground truth mask.
        prediction: A float array representing a predicted segmentation mask.
        ignore_label: An integer value representing a value that
        doesn't contribute to IoU.

    Returns:
        A float value representing IoU.
    """
    ignore_ground_truth_inv = ground_truth != ignore_label
    object_ground_truth = ground_truth == 1

    intersection = np.logical_and(
        np.logical_and(prediction, object_ground_truth), ignore_ground_truth_inv
    ).sum()
    union = np.logical_and(
        np.logical_or(prediction, object_ground_truth), ignore_ground_truth_inv
    ).sum()

    return intersection / union


def compute_noc(
    ious: list[np.ndarray], threshold: float = 0.9, max_clicks: int = 20
) -> float:
    """Computes the number of clicks (NoC).

    Args:
        ious: A list of a float array representing IoU.
        threshold: A float value representing the IoU threshold between predicted and
        ground truth masks.
        max_clicks: A integer value representing maximum clicks.

    Returns:
        A float value representing the average number of clicks required to achieve
        the threshold IoU.
    """

    def _get_noc(iou: np.ndarray) -> int:
        ok = iou >= threshold
        return cast(int, ok.argmax() + 1) if np.any(ok) else max_clicks

    scores = np.array([_get_noc(iou) for iou in ious], dtype=int)

    return scores.mean()
