import matplotlib.pyplot as plt
from dipcoatsubstrate.imgconstruct import (imgconstruct,
    ROIRectSubstrate)
subst = ROIRectSubstrate((600, 800), (500, 600))
img = imgconstruct((1200, 1600), subst, (300, 400))
plt.imshow(img) #doctest: +SKIP
