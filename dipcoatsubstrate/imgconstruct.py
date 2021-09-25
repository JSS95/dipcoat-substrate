"""
Module to construct the artificial image of the substrate.

"""

import cv2
import numpy as np

from numbers import Number
from typing import Tuple


__all__ = [
    "imgconstruct",
]


def imgconstruct(imgsize: Number, imgratio: Number,
                 roipt1: Tuple[int, int], roipt2: Tuple[int, int]) -> np.ndarray:
    """
    Constructs the artificial image of the substrate.

    .. warning::
        This function is not implemented yet.

    Parameters
    ==========

    imgsize : number
        Diagonal size of the image.

    imgratio : number
        Aspect ratio of the image.

    roipt1, roipt2 : (int, int)
        (x, y) location of two diagonal points of the ROI.

    Examples
    ========

    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt
        >>> from dipcoatsubstrate.imgconstruct import imgconstruct
        >>> img = imgconstruct(1000, 4/3, (250, 250), (500, 500))
        >>> plt.imshow(img) #doctest: +SKIP

    """
    def make_shape(size, ratio):
        x = size*ratio/np.sqrt(1 + ratio**2)
        y = size*ratio/np.sqrt(1 + ratio**2)
        return (int(y), int(x))

    imgshape = make_shape(imgsize, imgratio)
    img = cv2.cvtColor(np.full(imgshape, 255, np.uint8), cv2.COLOR_GRAY2BGR)

    img[:roipt1[1], :] = (0, 0, 0)

    roicolor = (255, 0, 0)
    cv2.rectangle(img, roipt1, roipt2, roicolor)

    return img
