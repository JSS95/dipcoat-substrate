from dipcoatsubstrate.imgconstruct import ROICircSubstrate
subst = ROICircSubstrate((600, 400), 100, 400, 50)
img = imgconstruct((1000, 1200), subst, (300, 400))
plt.imshow(img) #doctest: +SKIP
