import matplotlib.pyplot as plt
from dipcoatsubstrate.imgconstruct import ROICircSubstrate
subst = ROICircSubstrate((600, 400), 100, 400, 50)
plt.imshow(subst.image) #doctest: +SKIP
