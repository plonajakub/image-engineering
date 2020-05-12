from utils import *


def reveal_image(img_with_secret, nbits=1):
    jpeg_trailer = "1111" + "1111" + "1101" + "1001"  # b"\xFF\xD9"

    nbits = clamp(nbits, 1, 8)
    image = image_with_secret.flatten()

    message = ""
    i = 0
    while i < image_with_secret.size:
        byte = bin(image[i])[2:].zfill(8)
        message += byte[-nbits:]
        i += 1

    trailer_end_pos = len(jpeg_trailer)  # end index + 1
    while trailer_end_pos <= image_with_secret.size:
        if message[trailer_end_pos - len(jpeg_trailer): trailer_end_pos] == jpeg_trailer:
            break
        trailer_end_pos += 8

    img_bits_str = message[:trailer_end_pos]

    img_byte_chunks = [img_bits_str[i:i + 8] for i in range(0, len(img_bits_str), 8)]
    img_bytes_list = [bytes([int(byte, base=2)]) for byte in img_byte_chunks]
    img_bytes = b"".join(img_bytes_list)
    return img_bytes


if __name__ == "__main__":
    image = load_image("images/rembrandt.png")
    nbits = 1
    image_with_secret, _ = hide_image(image, "images/spanish.jpg", nbits)
    revealed_img = reveal_image(image_with_secret, nbits)

    revealed_img_path = "images/revealed_img_no_length.jpg"
    with open(revealed_img_path, "wb") as f_img:
        f_img.write(revealed_img)

    plt.imshow(load_image(revealed_img_path))
    plt.show()
