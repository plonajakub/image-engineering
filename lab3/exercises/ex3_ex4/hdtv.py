import cv2 as cv
import numpy as np


def downsample(img_1ch):
    return img_1ch[::2, ::2].copy()


def upsample(downs_img):
    ups_img = np.empty(shape=(downs_img.shape[0] * 2, downs_img.shape[1] * 2), dtype=np.uint8)
    for y in range(ups_img.shape[0]):
        for x in range(ups_img.shape[1]):
            ups_img[y][x] = downs_img[y // 2][x // 2]
    return ups_img


def get_each_channel_in_greyscale(img_bgr_local):
    img_b_3ch = img_bgr_local.copy()
    img_b_3ch[:, :, 1] = img_bgr_local[:, :, 0]
    img_b_3ch[:, :, 2] = img_bgr_local[:, :, 0]

    img_g_3ch = img_bgr_local.copy()
    img_g_3ch[:, :, 0] = img_bgr_local[:, :, 1]
    img_g_3ch[:, :, 2] = img_bgr_local[:, :, 1]

    img_r_3ch = img_bgr_local.copy()
    img_r_3ch[:, :, 0] = img_bgr_local[:, :, 2]
    img_r_3ch[:, :, 1] = img_bgr_local[:, :, 2]

    return img_b_3ch, img_g_3ch, img_r_3ch


img_bgr = cv.imread('../img/example.png')
if img_bgr is None:
    print('Error while reading the image')
    exit(-1)

img_b_grey, img_g_grey, img_r_grey = get_each_channel_in_greyscale(img_bgr)

# Original image
cv.namedWindow('original image', cv.WINDOW_NORMAL)
cv.imshow('original image', img_bgr)

# Brighter grey represents higher channel value
cv.namedWindow('blue channel in greyscale - original', cv.WINDOW_NORMAL)
cv.imshow('blue channel in greyscale - original', img_b_grey)

cv.namedWindow('green channel in greyscale - original', cv.WINDOW_NORMAL)
cv.imshow('green channel in greyscale - original', img_g_grey)

cv.namedWindow('red channel in greyscale - original', cv.WINDOW_NORMAL)
cv.imshow('red channel in greyscale - original', img_r_grey)

cv.waitKey(0)
cv.destroyAllWindows()

img_yCrCb = cv.cvtColor(img_bgr, cv.COLOR_BGR2YCrCb)

# to yCbCr
# img_yCbCr = img_yCrCb.copy()
# img_yCbCr[:, :, 1] = img_yCrCb[:, :, 2]
# img_yCbCr[:, :, 2] = img_yCrCb[:, :, 1]

img_y = img_yCrCb[:, :, 0]
img_cr = img_yCrCb[:, :, 1]
img_cb = img_yCrCb[:, :, 2]

d_img_cr = downsample(img_cr)
d_img_cb = downsample(img_cb)

u_img_cr = upsample(d_img_cr)
u_img_cb = upsample(d_img_cb)

received_img_yCrCb = np.empty(shape=img_yCrCb.shape, dtype=np.uint8)
received_img_yCrCb[:, :, 0] = img_y
received_img_yCrCb[:, :, 1] = u_img_cr
received_img_yCrCb[:, :, 2] = u_img_cb

received_img_bgr = cv.cvtColor(received_img_yCrCb, cv.COLOR_YCrCb2BGR)
received_img_b_grey, received_img_g_grey, received_img_r_grey = get_each_channel_in_greyscale(received_img_bgr)

# Received image
cv.namedWindow('received image', cv.WINDOW_NORMAL)
cv.imshow('received image', received_img_bgr)

# Brighter grey represents higher channel value
cv.namedWindow('blue channel in greyscale - received', cv.WINDOW_NORMAL)
cv.imshow('blue channel in greyscale - received', received_img_b_grey)

cv.namedWindow('green channel in greyscale - received', cv.WINDOW_NORMAL)
cv.imshow('green channel in greyscale - received', received_img_g_grey)

cv.namedWindow('red channel in greyscale - received', cv.WINDOW_NORMAL)
cv.imshow('red channel in greyscale - received', received_img_r_grey)

cv.waitKey(0)
cv.destroyAllWindows()

img_bgr_int16 = np.array(img_bgr, dtype=np.int16)  # int16 for negative values
received_img_bgr_int16 = np.array(received_img_bgr, dtype=np.int16)
mse_imgs = (np.square(img_bgr_int16 - received_img_bgr_int16)).mean(axis=None)
print("MSE between images: %.4f" % mse_imgs)
