#!/usr/bin/env python3
import numpy

# PPM file header
ppm_ascii_header = ''  # TODO: implement
ppm_binary_header = ''  # TODO: implement

# Image data
image = numpy.array([], dtype=numpy.uint8)  # TODO: implement

# Save the PPM image as an ASCII file
with open('lab4-ascii.ppm', 'w') as fh:
    fh.write(ppm_ascii_header)
    image.tofile(fh, ' ')

# Save the PPM image as a binary file
with open('lab4-binary.ppm', 'wb') as fh:
    fh.write(bytearray(ppm_binary_header, 'ascii'))
    image.tofile(fh)
