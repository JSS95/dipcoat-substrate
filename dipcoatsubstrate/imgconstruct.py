"""
Module to construct the artificial image of the substrate.

"""

import cv2
import numpy as np
from typing import Union, Tuple


__all__ = [
    "imgconstruct",
]


def imgconstruct(imgsize: Union[int, float], imgratio: Union[int, float],
                 roisize: Union[int, float], roiratio: Union[int, float],
                 roiloc: Tuple[int, int]):
    """
    Constructs the artificial image of the substrate.

    Parameters
    ==========

    imgsize : number
        Diagonal size of the image.

    imgratio : number
        Aspect ratio of the image.

    roisize : number
        Diagonal size of the ROI.

    roiratio : number
        Aspect ratio of the ROI.

    roiloc : (int, int)
        (x, y) location of upper left point of the ROI.

    Examples
    ========

    .. plot::
        :include-source:

        >>> from dipcoatsubstrate.imgconstruct import imgconstruct
        >>> img = imgconstruct(1000, 4/3, 250, 4/3, (250, 250))
        >>> plt.imshow(img) #doctest: +SKIP

    """
    def make_shape(size, ratio):
        x = size*ratio/np.sqrt(1 + ratio**2)
        y = size*ratio/np.sqrt(1 + ratio**2)
        return (int(y), int(x))

    imgshape = make_shape(imgsize, imgratio)
    img = cv2.cvtColor(np.full(imgshape, 255, np.uint8), cv2.COLOR_GRAY2BGR)

    roi_y, roi_x = make_shape(roisize, roiratio)
    color = (255, 0, 0)
    cv2.rectangle(img, roiloc, (roiloc[0] + roi_x, roiloc[1] + roi_y), color)

    return img
