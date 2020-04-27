#!/usr/bin/env python3
import numpy

colors_in_batch = 128
batches = 7
img_width = batches * colors_in_batch
img_height = 512
img_px_size = img_width * img_height
color_palette = 255
ws = ' '
cd_header = ws + str(img_width) + ws + str(img_height) + ws + str(color_palette) + ws

# PPM file header
ppm_ascii_header = 'P3' + cd_header
ppm_binary_header = 'P6' + cd_header

# Image data
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

# Save the PPM image as an ASCII file
with open('lab4-ascii.ppm', 'w') as fh:
    fh.write(ppm_ascii_header)
    image.tofile(fh, ' ')

# Save the PPM image as a binary file
with open('lab4-binary.ppm', 'wb') as fh:
    fh.write(bytearray(ppm_binary_header, 'ascii'))
    image.tofile(fh)
