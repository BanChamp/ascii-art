from PIL import Image

# Define ASCII characters from darkest to lightest.
ASCII_CHARS = "@B%8WM#*oahkbdpwmZO0QCJYXzcvnxrjft/\|()1{}[]-_+~<>i!lI;:,\^`'. "
ASCII_CHARS_REVERSED = ASCII_CHARS[::-1]  # Reversed for brightness mapping

def scale_image(image, new_width=100):
    """Resizes an image while preserving its aspect ratio."""
    original_width, original_height = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)
    return image.resize((new_width, new_height))

def convert_to_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii_chars(image, range_width=25):
    """Maps each pixel to an ASCII char based on brightness."""
    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[pixel_value // range_width] for pixel_value in pixels_in_image]
    return ''.join(pixels_to_chars)

def convert_image_to_ascii(image, new_width=100, brightness_factor=1.0):
    image = scale_image(image, new_width)
    image = convert_to_grayscale(image)
    image = Image.eval(image, lambda x: int(x / brightness_factor))
    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)
    return '\n'.join(pixels_to_chars[i:i+new_width] for i in range(0, len_pixels_to_chars, new_width))

def save_ascii_art_to_file(ascii_art, output_filepath):
    with open(output_filepath, 'w') as f:
        f.write(ascii_art)

def handle_image_conversion(image_filepath, new_width=100, brightness_factor=1.0, save_to_file=False, output_filepath="output.txt"):
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    image_ascii = convert_image_to_ascii(image, new_width, brightness_factor)

    if save_to_file:
        save_ascii_art_to_file(image_ascii, output_filepath)
    else:
        print(image_ascii)

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_image> [new_width] [brightness_factor] [output_filepath]")
    else:
        image_file_path = sys.argv[1]
        new_width = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        brightness_factor = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        output_filepath = sys.argv[4] if len(sys.argv) > 4 else "output.txt"
        handle_image_conversion(image_file_path, new_width, brightness_factor, True, output_filepath)
