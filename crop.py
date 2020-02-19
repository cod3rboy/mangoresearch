import os
from utils import get_file_paths
from PIL import JpegImagePlugin, Image


# Get the path to current working directory
working_dir = os.getcwd()

# Get all file paths in current working directory
file_paths = get_file_paths(working_dir, '.jpg')

# Get the dimensions of each image file.
widths = list()
heights = list()
for i in range(0, len(file_paths)):
    img = Image.open(file_paths[i])
    w, h = img.size
    widths.append(w)
    heights.append(h)

# Calculate the minimum of each dimension
min_width = min(widths)
print("Minimum Width: " + str(min_width))
min_height = min(heights)
print("Minimum Height: " + str(min_height))

# Crop each image and save it
output_dir = 'cropped'
for i in range(0, len(file_paths)):
    img = Image.open(file_paths[i])
    # Get original width and height of image
    w, h = img.size
    if w == min_width:
        print("Minimum width image file path : " + file_paths[i])
    if h == min_height:
        print("Minimum height image file path : " + file_paths[i])
    # Calculate aspect ratio of image
    aspect_ratio = h / w
    # Calculate new width and height preserving aspect ratio
    c_width = min_width
    c_height = int(min_width * aspect_ratio)
    # Resize image to new dimensions
    resized_img = img.resize((c_width, c_height))
    # Calculate corners for cropping resized image
    left = (c_width - min_width) / 2
    top = abs(c_height - min_height) / 2
    right = left + min_width
    bottom = top + min_height
    cropped_img = resized_img.crop((left, top, right, bottom))
    # Save cropped image
    file_dir = os.path.dirname(file_paths[i])
    file_name = os.path.basename(file_paths[i])
    output_path = os.path.join(file_dir, output_dir)
    os.makedirs(output_path, exist_ok=True)
    cropped_img.save(os.path.join(output_path, file_name), 'JPEG')
