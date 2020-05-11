original_image = load_image("images/rembrandt.png")
message = "Ani połowy spośród was nie znam nawet do połowy tak dobrze, jak bym pragnął; a mniej niż połowę z was lubię o połowę mniej, niż zasługujecie."
message = encode_as_binary_array(message)
image_with_message = hide_message(original_image, message, 1)
save_image("images/image_with_hidden_bilbo_quote.png", image_with_message)
