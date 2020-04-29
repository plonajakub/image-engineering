#!/usr/bin/env python3
import zlib
import numpy
import lab4_utils as l4utils
import cv2 as cv

# 0. Image data
colors_in_batch = 128
batches = 7
img_width = batches * colors_in_batch
img_height = 512
img_px_size = img_width * img_height
r_versor = numpy.array([1, 0, 0], dtype=numpy.uint8)
g_versor = numpy.array([0, 1, 0], dtype=numpy.uint8)
b_versor = numpy.array([0, 0, 1], dtype=numpy.uint8)
step_size = 256 // colors_in_batch
current_color = numpy.array([0, 0, 0], dtype=numpy.uint8)
image = numpy.empty(shape=(img_height, img_width, 3), dtype=numpy.uint8)
for batch_idx in range(batches):
    current_op = None
    if batch_idx == 0:
        current_op = b_versor
    elif batch_idx == 1:
        current_op = g_versor
    elif batch_idx == 2:
        current_op = -b_versor
    elif batch_idx == 3:
        current_op = r_versor
    elif batch_idx == 4:
        current_op = -g_versor
    elif batch_idx == 5:
        current_op = b_versor
    elif batch_idx == 6:
        current_op = g_versor
    for step_idx in range(colors_in_batch):
        if step_idx == 0:
            current_color += (step_size - 1) * current_op
        else:
            current_color += step_size * current_op
        image[:, batch_idx * colors_in_batch + step_idx, :] = current_color

# image: image, shape(height, width, 3), type(uint8)
img_bgr = cv.cvtColor(image, cv.COLOR_RGB2BGR)

label_before_compress = 'Before compression'
cv.namedWindow(label_before_compress, cv.WINDOW_NORMAL)
cv.imshow(label_before_compress, img_bgr)
# cv.waitKey(0)
# cv.destroyAllWindows()

# 1. Convert RGB to YCbCr
img_yCrCb = cv.cvtColor(img_bgr, cv.COLOR_BGR2YCrCb)
img_y = img_yCrCb[:, :, 0]
img_Cr = img_yCrCb[:, :, 1]
img_Cb = img_yCrCb[:, :, 2]


# 2. Downsampling on Cb Cr
def downsample(img_1ch, ratio):
    return img_1ch[::ratio, ::ratio].copy()


du_sample_ratio = 4
img_Cr_downsample = downsample(img_Cr, du_sample_ratio)
img_Cb_downsample = downsample(img_Cb, du_sample_ratio)


# 3. Produce 8x8 blocks
def extract_blocks_8(img_1ch):
    n_y_step = img_1ch.shape[0] // 8
    n_x_step = img_1ch.shape[1] // 8
    blocks = numpy.empty(shape=(n_y_step * n_x_step, 8, 8), dtype=numpy.uint8)
    block_idx = 0
    for y in range(n_y_step):
        for x in range(n_x_step):
            blocks[block_idx, :, :] = img_1ch[y * 8:(y + 1) * 8, x * 8:(x + 1) * 8]
            block_idx += 1
    return blocks


img_y_8blocks = extract_blocks_8(img_y)
img_Cr_ds_8blocks = extract_blocks_8(img_Cr_downsample)
img_Cb_ds_8blocks = extract_blocks_8(img_Cb_downsample)


# 4. Calculate DCT on each block
def dct_on_each_block(img_1ch_8b):
    result = numpy.empty(shape=img_1ch_8b.shape, dtype=numpy.float64)
    for i in range(img_1ch_8b.shape[0]):
        result[i, :, :] = l4utils.dct2(img_1ch_8b[i, :, :])
    return result


img_y_8b_dct = dct_on_each_block(img_y_8blocks)
img_Cr_ds_8b_dct = dct_on_each_block(img_Cr_ds_8blocks)
img_Cb_ds_8b_dct = dct_on_each_block(img_Cb_ds_8blocks)


# 5. Divide each block by quantisation matrix
# 6. Round each block to integers
def div_each_block_by_qmat(img_1ch_8b_dct, q_type, qf):
    result = numpy.empty(shape=img_1ch_8b_dct.shape, dtype=numpy.int16)
    for i in range(img_1ch_8b_dct.shape[0]):
        if q_type == 'qy':
            res = img_1ch_8b_dct[i, :, :] / l4utils.QY(qf)
        else:
            res = img_1ch_8b_dct[i, :, :] / l4utils.QC(qf)
        result[i, :, :] = numpy.around(res)
    return result


quality_factor = 95
img_y_8b_dct_qr = div_each_block_by_qmat(img_y_8b_dct, 'qy', quality_factor)
img_Cr_ds_8b_dct_qr = div_each_block_by_qmat(img_Cr_ds_8b_dct, 'qc', quality_factor)
img_Cb_ds_8b_dct_qr = div_each_block_by_qmat(img_Cb_ds_8b_dct, 'qc', quality_factor)


# 7. Zig Zag
def zigzag(img_1ch):
    result = [[] for _ in range(img_1ch.shape[0] + img_1ch.shape[1] - 1)]
    for y in range(img_1ch.shape[0]):
        for x in range(img_1ch.shape[1]):
            idx_sum = y + x
            if idx_sum % 2 == 0:
                result[idx_sum].insert(0, img_1ch[y, x])
            else:
                result[idx_sum].append(img_1ch[y, x])
    flattened_numpy_result = numpy.empty(shape=img_1ch.shape[0] * img_1ch.shape[1], dtype=numpy.uint8)

    next_idx = 0
    for sublist in result:
        for item in sublist:
            flattened_numpy_result[next_idx] = item
            next_idx += 1

    return flattened_numpy_result


img_y_zz = zigzag(img_y)
img_Cr_ds_zz = zigzag(img_Cr_downsample)
img_Cb_ds_zz = zigzag(img_Cb_downsample)

# 8. Flatten, concatenate, compress and calculate the size -- how many bytes?
img_flat_concat = numpy.empty(shape=img_y_zz.shape[0] + img_Cr_ds_zz.shape[0] + img_Cb_ds_zz.shape[0],
                              dtype=numpy.uint8)
ifc_lim_0 = 0
ifc_lim_1 = ifc_lim_0 + img_y_zz.size
ifc_lim_2 = ifc_lim_1 + img_Cr_ds_zz.size
ifc_lim_3 = ifc_lim_2 + img_Cb_ds_zz.size
img_flat_concat[ifc_lim_0:ifc_lim_1] = img_y_zz
img_flat_concat[ifc_lim_1:ifc_lim_2] = img_Cr_ds_zz
img_flat_concat[ifc_lim_2:ifc_lim_3] = img_Cb_ds_zz

cmpsd_img_flat_concat = zlib.compress(img_flat_concat.tobytes(), level=9)
print('Approximated size of the compressed image: {0} B'.format(len(cmpsd_img_flat_concat)))


# 7'. Undo Zig Zag
# We can skip it in this exercise!

# 6'. Nothing to do here   ¯\_(ツ)_/¯
# For the next step, just reuse the rounded data obtained in step 6.

# 5'. Reverse division by quantisation matrix -- multiply
def mult_each_block_by_qmat(img_1ch_8b_dct_qr, q_type, qf):
    result = numpy.empty(shape=img_1ch_8b_dct_qr.shape, dtype=numpy.int16)
    for i in range(img_1ch_8b_dct_qr.shape[0]):
        if q_type == 'qy':
            result[i, :, :] = img_1ch_8b_dct_qr[i, :, :] * l4utils.QY(qf)
        else:
            result[i, :, :] = img_1ch_8b_dct_qr[i, :, :] * l4utils.QC(qf)
    return result


r_img_y_8b_dct_qr = mult_each_block_by_qmat(img_y_8b_dct_qr, 'qy', quality_factor)
r_img_Cr_ds_8b_dct_qr = mult_each_block_by_qmat(img_Cr_ds_8b_dct_qr, 'qc', quality_factor)
r_img_Cb_ds_8b_dct_qr = mult_each_block_by_qmat(img_Cb_ds_8b_dct_qr, 'qc', quality_factor)


# 4'. Reverse DCT
def idct_on_each_block(img_1ch_8b_dct):
    result = numpy.empty(shape=img_1ch_8b_dct.shape, dtype=numpy.uint8)
    for i in range(img_1ch_8b_dct.shape[0]):
        res = l4utils.idct2(img_1ch_8b_dct[i, :, :])
        result[i, :, :] = numpy.around(res)
    return result


r_img_y_8b_dct = idct_on_each_block(r_img_y_8b_dct_qr)
r_img_Cr_ds_8b_dct = idct_on_each_block(r_img_Cr_ds_8b_dct_qr)
r_img_Cb_ds_8b_dct = idct_on_each_block(r_img_Cb_ds_8b_dct_qr)


# 3'. Combine 8x8 blocks to original image
# TODO: implement

# 2'. Upsampling on Cb Cr
def upsample(downs_img, ratio):
    ups_img = numpy.empty(shape=(downs_img.shape[0] * ratio, downs_img.shape[1] * ratio), dtype=numpy.uint8)
    for y in range(ups_img.shape[0]):
        for x in range(ups_img.shape[1]):
            ups_img[y][x] = downs_img[y // ratio][x // ratio]
    return ups_img


img_Cr_upsample = upsample(img_Cr_downsample, du_sample_ratio)
img_Cb_upsample = upsample(img_Cb_downsample, du_sample_ratio)

# 1'. Convert YCbCr to RGB
reconstructed_img_yCrCb = numpy.empty(shape=img_yCrCb.shape, dtype=numpy.uint8)
reconstructed_img_yCrCb[:, :, 0] = img_y
reconstructed_img_yCrCb[:, :, 1] = img_Cr_upsample
reconstructed_img_yCrCb[:, :, 2] = img_Cb_upsample

reconstructed_img_bgr = cv.cvtColor(reconstructed_img_yCrCb, cv.COLOR_YCrCb2BGR)

# 0'. Save the decoded image -- as PPM or PNG
cv.imwrite('lab4-jpeg-result.png', reconstructed_img_bgr, [cv.IMWRITE_PNG_COMPRESSION, 9])
label_after_compress = 'After compression'
cv.namedWindow(label_after_compress, cv.WINDOW_NORMAL)
cv.imshow(label_after_compress, reconstructed_img_bgr)
cv.waitKey(0)
cv.destroyAllWindows()

# Notatka do zadania 4
# Bez próbkowania: rozmiar - 15589 B, brak zauważalnej różnicy w wyglądzie
# Co 2 piksel: rozmiar - 9224 B, brak zauważalnej różnicy w wyglądzie
# Co 4 piksel: rozmiar - 7129 B, brak zauważalnej różnicy w wyglądzie
# Co 64 piksel: rozmiar - 5311 B, ciężko nie zauważyć różnicy :)
# Podsumowując, etap downsamplingu istotnie zmniejsza wielkość pliku przy niezauważalnych stratach jakości zdjęcia
# (zakładając niewielki krok próbkowania).
# Zbyt rzadkie próbkowanie nie przynosi znaczącego zysku w zajętości miejsca na dysku, zaś może znacznie wpłynąć
# na jakość obrazka.
# Wydaje się, że krok równy 4px jest krokiem dobrym (strata nie jest jeszcze widoczna).
