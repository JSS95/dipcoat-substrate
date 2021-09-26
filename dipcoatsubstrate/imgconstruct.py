"""
Module to construct the artificial image of the substrate.

"""

from abc import ABCMeta, abstractmethod, abstractclassmethod
import cv2
import numpy as np

from typing import Tuple, Optional


__all__ = [
    "ROISubstrate",
    "ROIRectSubstrate",
    "ROICircSubstrate",
    "imgconstruct",
]


class ROISubstrate(metaclass=ABCMeta):
    """
    Abstract base class for ROI image containing the substrate.

    Subclass must define :func:`image()<ROISubstrate.image>` property, and
    :func:`random()<ROISubstrate.random>` method.

    Parameters
    ==========

    shape
        (height, width) of the ROI.

    Attributes
    ==========

    shape : tuple
        (height, width) of the ROI.

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

    @abstractclassmethod
    def random(cls, shape: Tuple[int, int], seed: Optional[int] = None):
        """
        Return the randomized instance.

        Parameters
        ==========

        shape
            Shape of the full image.

        seed
            Randomizing seed.

        Returns
        =======

        ROISubstrate

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
        (height, width) of the ROI.

    substshape
        (height, width) of the substrate.

    Attributes
    ==========

    substshape : tuple
        (height, width) of the substrate.

    Examples
    ========

    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt
        >>> from dipcoatsubstrate.imgconstruct import ROIRectSubstrate
        >>> subst = ROIRectSubstrate((600, 800), (500, 600))
        >>> plt.imshow(subst.image) #doctest: +SKIP

    """
    def __init__(self, shape: Tuple[int, int], substshape: Tuple[int, int]):
        super().__init__(shape)

        if shape[0] < substshape[0]:
            raise SubstrateError("Substrate is taller than the ROI")
        if shape[1] < substshape[1]:
            raise SubstrateError("Substrate is wider than the ROI")
        self.substshape = substshape

    @property
    def image(self):
        _, roi_w = self.shape
        subst_h, subst_w = self.substshape
        width_margin = int((roi_w - subst_w)/2)
        ret = self.blank_image.copy()
        ret[:subst_h, width_margin:-width_margin] = (0, 0, 0)
        return ret

    @classmethod
    def random(cls, shape: Tuple[int, int], seed: Optional[int] = None):
        np.random.seed(seed)
        h_ratio, w_ratio = np.random.uniform(0.5, 0.9, 2)
        substshape = (int(shape[0]*h_ratio), int(shape[1]*w_ratio))
        return cls(shape, substshape)


class ROICircSubstrate(ROISubstrate):
    """
    ROI image containing the circular substrate.

    Parameters
    ==========

    shape
        (height, width) of the ROI.

    r
        Radius of the circular part.

    l, w
        Length and width of the branch part.

    Attributes
    ==========

    r : int
        Radius of the circular part.

    l, w : int
        Length and width of the branch part.

    Examples
    ========

    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt
        >>> from dipcoatsubstrate.imgconstruct import ROICircSubstrate
        >>> subst = ROICircSubstrate((600, 400), 100, 400, 50)
        >>> plt.imshow(subst.image) #doctest: +SKIP

    """
    def __init__(self, shape: Tuple[int, int], r: int, l: int, w: int):
        super().__init__(shape)

        if 2*r < w:
            raise SubstrateError("Substrate branch is wider than the circle")
        if min(shape) < 2*r:
            raise SubstrateError("Substrate is larger than the ROI")
        if shape[0] < l + r:
            raise SubstrateError("Substrate is longer than the ROI")
        if shape[1] < w:
            raise SubstrateError("Substrate is wider than the ROI")

        self.r = r
        self.l = l
        self.w = w

    @property
    def image(self):
        ret = self.blank_image.copy()
        center = (int(self.shape[1]/2), self.l)
        cv2.circle(ret, center, self.r, (0, 0, 0), -1)

        p1 = (int(self.shape[1]/2 - self.w/2), 0)
        p2 = (int(self.shape[1]/2 + self.w/2), self.l)
        cv2.rectangle(ret, p1, p2, (0, 0, 0), -1)

        return ret

    @classmethod
    def random(cls, shape: Tuple[int, int], seed: Optional[int] = None):
        np.random.seed(seed)
        r = int(np.random.randint(min(shape)/4, min(shape))/2)
        np.random.seed(seed)
        l = np.random.randint(max(shape[0]/2 - r, 0), shape[0] - r)
        np.random.seed(seed)
        w = np.random.randint(r/10, 2*r)
        return cls(shape, r, l, w)

def imgconstruct(imgshape: Tuple[int, int], substrate: ROISubstrate,
                 roipt: Tuple[int, int]) -> np.ndarray:
    """
    Constructs the artificial image of the substrate.

    .. warning::
        This function is not fully implemented yet.

    Parameters
    ==========

    imgshape
        (height, width) of the image.

    substrate
        ROI image containing the substrate.

    roipt
        (x, y) coordinates of top left point of the ROI.

    Examples
    ========

    .. plot::
        :include-source:
        :context: reset

        >>> import matplotlib.pyplot as plt
        >>> from dipcoatsubstrate.imgconstruct import (imgconstruct,
        ...     ROIRectSubstrate)
        >>> subst = ROIRectSubstrate((600, 800), (500, 600))
        >>> img = imgconstruct((1200, 1600), subst, (300, 400))
        >>> plt.imshow(img) #doctest: +SKIP

    .. plot::
        :include-source:
        :context: close-figs

        >>> from dipcoatsubstrate.imgconstruct import ROICircSubstrate
        >>> subst = ROICircSubstrate((600, 400), 100, 400, 50)
        >>> img = imgconstruct((1000, 1200), subst, (300, 400))
        >>> plt.imshow(img) #doctest: +SKIP

    """
    img = cv2.cvtColor(np.full(imgshape, 255, np.uint8), cv2.COLOR_GRAY2BGR)

    roipt2 = (roipt[0] + substrate.shape[0], roipt[1] + substrate.shape[1])
    img[roipt[0]:roipt2[0], roipt[1]:roipt2[1]] = substrate.image

    img[:roipt[0]] = (0, 0, 0)

    return img
