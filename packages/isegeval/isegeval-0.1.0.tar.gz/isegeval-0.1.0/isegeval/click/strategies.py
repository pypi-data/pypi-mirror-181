import numpy as np
from scipy.ndimage import distance_transform_edt

from .strategy import Click, Strategy


class GreatestErrorRegion(Strategy):
    """A strategy to click the greatest error region.

    Args:
        ground_truth_mask: A float array representing a ground truth mask.
        ignore_label: An integer value representing a value that
        doesn't contribute to prediction.
    """

    def __init__(self, ground_truth_mask: np.ndarray, ignore_label: int = -1) -> None:
        self.ground_truth_mask = ground_truth_mask
        self.clickable_mask = ground_truth_mask != ignore_label
        self.not_clicked_mask = np.ones_like(ground_truth_mask)

    def click(self, segmentation_mask: np.ndarray) -> Click:
        """Returns the point to click.

        Args:
            segmentation_mask: A float array representing a predicted segmentation mask.

        Returns:
            A click object representing the point to click.
        """
        fn_mask = np.logical_and(
            np.logical_and(self.ground_truth_mask, np.logical_not(segmentation_mask)),
            self.clickable_mask,
        )
        fp_mask = np.logical_and(
            np.logical_and(np.logical_not(self.ground_truth_mask), segmentation_mask),
            self.clickable_mask,
        )

        fn_mask = np.pad(fn_mask, ((1, 1), (1, 1)), "constant")
        fp_mask = np.pad(fp_mask, ((1, 1), (1, 1)), "constant")

        fn_mask_dt = distance_transform_edt(fn_mask.astype(np.uint8))[1:-1, 1:-1]
        fp_mask_dt = distance_transform_edt(fp_mask.astype(np.uint8))[1:-1, 1:-1]

        fn_mask_dt = fn_mask_dt * self.not_clicked_mask
        fp_mask_dt = fp_mask_dt * self.not_clicked_mask

        fn_max_dist = np.max(fn_mask_dt)
        fp_max_dist = np.max(fp_mask_dt)

        is_positive = fn_max_dist > fp_max_dist

        if is_positive:
            coords_y, coords_x = np.where(fn_mask_dt == fn_max_dist)  # coords is [y, x]
        else:
            coords_y, coords_x = np.where(fp_mask_dt == fp_max_dist)  # coords is [y, x]

        y, x = coords_y[0], coords_x[0]
        self.not_clicked_mask[y, x] = False
        return Click(x=x, y=y, is_positive=is_positive)
