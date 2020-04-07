import cv2 as cv
import numpy as np

img = cv.imread('../img/example.png')
if img is None:
    print('Error while reading the image')
    exit(-1)

kernel = np.array([
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1],
])
filtered_image = cv.filter2D(img, -1, kernel=kernel)

cv.imshow('high-pass-filer', filtered_image)
cv.waitKey(0)
cv.destroyAllWindows()
