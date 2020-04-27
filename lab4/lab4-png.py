#!/usr/bin/env python3
import numpy
import struct
import zlib

# Image data
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

raw_img = image.tobytes()
pad_img = b''
for row_idx in range(img_height):
    pad_img += b'\x00'
    pad_img += raw_img[row_idx * img_width * 3: (row_idx + 1) * img_width * 3]


# Construct signature
png_file_signature = b'\x89PNG\r\n\x1a\n'

# Construct header
header_id = b'IHDR'
header_content = struct.pack('!IIBBBBB', img_width, img_height, 8, 2, 0, 0, 0)
header_size = struct.pack('!I', len(header_content))
header_crc = struct.pack('!I', zlib.crc32(header_id + header_content))
png_file_header = header_size + header_id + header_content + header_crc

# Construct data
data_id = b'IDAT'
data_content = zlib.compress(pad_img, level=9)
data_size = struct.pack('!I', len(data_content))
data_crc = struct.pack('!I', zlib.crc32(data_id + data_content))
png_file_data = data_size + data_id + data_content + data_crc

# Consruct end
end_id = b'IEND'
end_content = b''
end_size = struct.pack('!I', len(end_content))
end_crc = struct.pack('!I', zlib.crc32(end_id + end_content))
png_file_end = end_size + end_id + end_content + end_crc

# Save the PNG image as a binary file
with open('lab4.png', 'wb') as fh:
    fh.write(png_file_signature)
    fh.write(png_file_header)
    fh.write(png_file_data)
    fh.write(png_file_end)
