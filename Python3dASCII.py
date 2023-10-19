from PIL import Image, ImageDraw
import argparse
import os

# Define ASCII characters and their corresponding shades from darkest to lightest.
ASCII_CHARS = '@%#*+=-:. '

def scale_image(image, new_width=100):
    original_width, original_height = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)
    return image.resize((new_width, new_height))

def convert_to_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii_chars(image, range_width=25):
    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[pixel_value // range_width] for pixel_value in pixels_in_image]
    return ''.join(pixels_to_chars)

def convert_image_to_ascii(image, new_width=100, shading=True):
    image = scale_image(image, new_width)
    image = convert_to_grayscale(image)

    if shading:
        draw = ImageDraw.Draw(image)
        for x in range(image.width):
            for y in range(image.height):
                pixel_value = image.getpixel((x, y))
                shading_char = ASCII_CHARS[pixel_value // 25]
                draw.text((x, y), shading_char, fill="white")

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)
    return '\n'.join(pixels_to_chars[i:i+new_width] for i in range(0, len_pixels_to_chars, new_width))

def save_ascii_art_to_file(ascii_art, output_filepath):
    with open(output_filepath, 'w') as f:
        f.write(ascii_art)

def handle_image_conversion(image_filepath, new_width=100, shading=True, save_to_file=False, output_filepath="output.txt"):
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    image_ascii = convert_image_to_ascii(image, new_width, shading)

    if save_to_file:
        save_ascii_art_to_file(image_ascii, output_filepath)
    else:
        print(image_ascii)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', type=str, help='Path to the image file')
    parser.add_argument('--width', type=int, default=100, help='Width for ASCII art (default: 100)')
    parser.add_argument('--shading', action='store_true', help='Add 3D shading to ASCII art')
    parser.add_argument('--output', type=str, help='Output file path (default: output.txt)')
    args = parser.parse_args()

    if os.path.exists(args.image_file):
        handle_image_conversion(args.image_file, args.width, args.shading, save_to_file=True, output_filepath=args.output)
    else:
        print(f"The image file '{args.image_file}' does not exist.")
