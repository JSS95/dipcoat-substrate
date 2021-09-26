import numpy as np
from dipcoatsubstrate.imgconstruct import ROIRectSubstrate

def test_ROIRectSubstrate():
    subst = ROIRectSubstrate((600, 800), (500, 600))
    assert subst.image.shape == (600, 800, 3)
    assert np.all(subst.image[:500, 100:700] == (0, 0, 0))
