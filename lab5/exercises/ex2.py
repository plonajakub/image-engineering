from utils import *

def mse(img1, img2):
    t_img1 = np.array(img1, dtype=np.int16).flatten()
    t_img2 = np.array(img2, dtype=np.int16).flatten()
    mse = (np.square(t_img1 - t_img2)).mean(axis=None)
    return mse

original_image = load_image("images/rembrandt.png")
orig_img_shape = original_image.shape
orig_img_nbytes = orig_img_shape[0] * orig_img_shape[1] * orig_img_shape[2]

text_to_hide = "Lorem bla bla bla"
nTexts = (0.8 * orig_img_nbytes) / len(encode_as_binary_array(text_to_hide)) # 1 bit coded per 1 img byte
text_to_hide *= math.ceil(nTexts)

message = encode_as_binary_array(text_to_hide)

mses = []
images = []
f, axs = plt.subplots(9, 1, figsize=(30, 30))
axs = axs.ravel()
for nbits in range(1, 9):
    image_with_message = hide_message(original_image, message, nbits)
    images.append(image_with_message)
    imgs_mse = mse(original_image, image_with_message)
    mses.append(imgs_mse)
    axs[nbits - 1].imshow(images[nbits - 1])
    axs[nbits - 1].set_title("nbits = " + str(nbits))

axs[-1].set_title("MSE vs nbits")
axs[-1].set_xlabel("nbits")
axs[-1].set_ylabel("MSE")
axs[-1].plot([i for i in range(1, 9)], mses)

plt.show()
