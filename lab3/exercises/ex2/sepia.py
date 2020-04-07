import cv2 as cv
import numpy as np

img = cv.imread('../img/example.png')
if img is None:
    print('Error while reading the image')
    exit(-1)

img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

t_matrix = np.array([
    [0.272, 0.534, 0.131],
    [0.349, 0.689, 0.168],
    [0.393, 0.769, 0.189],
])
t_img = np.array(img, dtype=np.float32)
t_img /= 255

for y in range(t_img.shape[0]):
    for x in range(t_img.shape[1]):
        t_img[y, x, :] = np.transpose(np.matmul(t_matrix, np.transpose(t_img[y, x, :])))

t_img = np.minimum(t_img, np.ones(t_img.shape))

cv.imshow('sepia', t_img)
cv.waitKey(0)
cv.destroyAllWindows()
