#!/usr/bin/env python3
import numpy

img_width = 512
img_height = 512
img_px_size = img_width * img_height
color_vector_rgb = [0, 255, 0]
color_palette = 255
ws = ' '
cd_header = ws + str(img_width) + ws + str(img_height) + ws + str(color_palette) + ws

# PPM file header
ppm_ascii_header = 'P3' + cd_header
ppm_binary_header = 'P6' + cd_header

# Image data
image = numpy.array([color_vector_rgb for i in range(img_width * img_height)], dtype=numpy.uint8)

# Save the PPM image as an ASCII file
with open('lab4-ascii.ppm', 'w') as fh:
    fh.write(ppm_ascii_header)
    image.tofile(fh, ' ')

# Save the PPM image as a binary file
with open('lab4-binary.ppm', 'wb') as fh:
    fh.write(bytearray(ppm_binary_header, 'ascii'))
    image.tofile(fh)
