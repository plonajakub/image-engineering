from utils import *


def hide_message(image, message, nbits=1, spos=0):
    """Hide a message in an image (LSB).

    nbits: number of least significant bits
    spos: offset for message write position in the image
    """
    nbits = clamp(nbits, 1, 8)
    shape = image.shape
    image = image.flatten()
    if len(message) > (len(image) - spos) * nbits:
        raise ValueError("Message is to long :(")

    chunks = [message[i:i + nbits] for i in range(0, len(message), nbits)]
    for i, chunk in enumerate(chunks):
        byte = bin(image[i + spos])[2:].zfill(8)
        new_byte = byte[:-nbits] + chunk
        new_byte += "0" * (8 - len(new_byte))  # In case of writing incomplete chunk
        image[i + spos] = int(new_byte, 2)

    return image.reshape(shape)


def reveal_message(image, nbits=1, length=0, spos=0):
    """Reveal the hidden message.

    nbits: number of least significant bits
    length: length of the message in bits.
    spos: offset for message read position in the image
    """
    nbits = clamp(nbits, 1, 8)
    image = image.flatten()
    length_in_pixels = math.ceil(length / nbits)
    if len(image) < (length_in_pixels + spos) or length_in_pixels <= 0:
        length_in_pixels = len(image) - spos

    message = ""
    i = 0
    while i < length_in_pixels:
        byte = bin(image[i + spos])[2:].zfill(8)
        message += byte[-nbits:]
        i += 1

    mod = length % nbits
    if mod != 0:
        message = message[:-(nbits - mod)]  # Discard additional bits
    return message


if __name__ == "__main__":
    original_image = load_image("images/rembrandt.png")
    message = "It's a miracle!"
    print("Original message: ", message)
    n = 3
    spos = 30

    message = encode_as_binary_array(message)
    image_with_message = hide_message(image=original_image, message=message, nbits=n, spos=spos)

    secret_message = decode_from_binary_array(
        reveal_message(image=image_with_message, nbits=n, length=len(message), spos=spos))

    print("Secret message: ", secret_message)
