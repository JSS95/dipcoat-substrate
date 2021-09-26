import matplotlib.pyplot as plt
from dipcoatsubstrate.imgconstruct import ROIRectSubstrate
subst = ROIRectSubstrate((600, 800), (500, 600))
plt.imshow(subst.image) #doctest: +SKIP
