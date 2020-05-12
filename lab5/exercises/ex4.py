from utils import *


def reveal_image(img_with_secret, hidden_img_len, nbits=1):
    img_bits_str = reveal_message(img_with_secret, nbits, hidden_img_len)
    img_byte_chunks = [img_bits_str[i:i + 8] for i in range(0, len(img_bits_str), 8)]
    img_bytes_list = [bytes([int(byte, base=2)]) for byte in img_byte_chunks]
    img_bytes = b"".join(img_bytes_list)
    return img_bytes


if __name__ == "__main__":
    image = load_image("images/rembrandt.png")
    nbits = 1
    image_with_secret, length_of_secret = hide_image(image, "images/spanish.jpg", nbits)
    revealed_img = reveal_image(image_with_secret, length_of_secret, nbits)

    revealed_img_path = "images/revealed_img.jpg"
    with open(revealed_img_path, "wb") as f_img:
        f_img.write(revealed_img)

    plt.imshow(load_image(revealed_img_path))
    plt.show()
