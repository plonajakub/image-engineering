#!/usr/bin/env python3
import numpy
import struct
import zlib

# Image data
image = numpy.array([[[255,   0,   0], [  0, 255,  0]],
                     [[  0,   0, 255], [ 55,  55,  0]]],
                    dtype=numpy.uint8)  # TODO: implement

# Construct signature
png_file_signature = ''  # TODO: implement

# Construct header
header_id = ''  # TODO: implement
header_content = ''  # TODO: implement
header_size = ''  # TODO: implement
header_crc = ''  # TODO: implement
png_file_header = header_size + header_id + header_content + header_crc

# Construct data
data_id = ''  # TODO: implement
data_content = ''  # TODO: implement
data_size = ''  # TODO: implement
data_crc = ''  # TODO: implement
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
