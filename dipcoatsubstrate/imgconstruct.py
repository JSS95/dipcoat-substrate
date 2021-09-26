"""
Module to construct the artificial image of the substrate.

"""

from abc import ABCMeta, abstractmethod
import cv2
import numpy as np

from typing import Tuple


__all__ = [
    "ROISubstrate",
    "ROIRectSubstrate",
    "imgconstruct",
]


class ROISubstrate(metaclass=ABCMeta):
    """
    Abstract base class for ROI image containing the substrate.

    Subclass must define :func:`image()<ROISubstrate.image>` property.

    Parameters
    ==========

    shape
        (width, height) of the ROI.

    Attributes
    ==========

    shape : tuple
        (width, height) of the ROI.

    blank_image : np.ndarray
        Image of the blank ROI without substrate.

    """
    def __init__(self, shape: Tuple[int, int]):
        self.shape = shape
        blankimg = np.full(shape, 255, np.uint8)
        self.blank_image = cv2.cvtColor(blankimg, cv2.COLOR_GRAY2BGR)

    @property
    @abstractmethod
    def image(self) -> np.ndarray:
        """
        Return the image of ROI with substrate drawn.

        """
        ...


class SubstrateError(Exception):
    pass


class ROIRectSubstrate(ROISubstrate):
    """
    ROI image containing the rectangular substrate.

    Parameters
    ==========

    shape
        (width, height) of the ROI.

    substshape
        (width, height) of the substrate.

    Attributes
    ==========

    substshape : tuple
        (width, height) of the substrate.

    Examples
    ========

    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt
        >>> from dipcoatsubstrate.imgconstruct import ROIRectSubstrate
        >>> subst = ROIRectSubstrate((600, 800), (200, 300))
        >>> plt.imshow(subst.image) #doctest: +SKIP

    """
    def __init__(self, shape: Tuple[int, int], substshape: Tuple[int, int]):
        super().__init__(shape)

        if shape[0] < substshape[0]:
            raise SubstrateError("Substrate is wider than the ROI")
        if shape[1] < substshape[1]:
            raise SubstrateError("Substrate is taller than the ROI")
        self.substshape = substshape

    @property
    def image(self):
        roi_w, _ = self.shape
        subst_w, subst_h = self.substshape
        width_margin = int((roi_w - subst_w)/2)
        ret = self.blank_image.copy()
        ret[:subst_h, width_margin:-width_margin] = (0, 0, 0)
        return ret


def imgconstruct(imgshape: Tuple[int, int], substrate: ROISubstrate,
                 roipt: Tuple[int, int]) -> np.ndarray:
    """
    Constructs the artificial image of the substrate.

    .. warning::
        This function is not fully implemented yet.

    Parameters
    ==========

    imgshape
        (width, height) of the image.

    substrate
        ROI image containing the substrate.

    roipt
        (x, y) coordinates of top left point of the ROI.

    Examples
    ========

    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt
        >>> from dipcoatsubstrate.imgconstruct import (imgconstruct,
        ...     ROIRectSubstrate)
        >>> subst = ROIRectSubstrate((600, 800), (200, 300))
        >>> img = imgconstruct((1200, 1600), subst, (300, 400))
        >>> plt.imshow(img) #doctest: +SKIP

    """
    img = cv2.cvtColor(np.full(imgshape, 255, np.uint8), cv2.COLOR_GRAY2BGR)

    roipt2 = (roipt[0] + substrate.shape[0], roipt[1] + substrate.shape[1])
    img[roipt[0]:roipt2[0], roipt[1]:roipt2[1]] = substrate.image

    return img
