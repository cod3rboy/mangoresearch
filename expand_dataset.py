## Python Script to expand dataset by enhancing existing images in dataset.

import os
import string
import random
from PIL import Image, ImageEnhance
from utils import get_file_paths

# Image Enhancemnet Parameters
CONTRAST = 1.5 # 0 : No Contrast Gray Image and 1 : Original Image
BRIGHTNESS = 1.5 # 0 : No Brightness and  > 1 : More Brightness
SHARPNESS = 1.5 # 0 : Blurness , 1 : No Sharpness , > 1 : Sharp Image
COLOR = 1.5 # 0 : No Color (Grayscale), 1 : Original Color , > 1 Saturated Color

# Whether to save both original and enhanced images to output or just enhanced image.
OUT_BOTH = False

print("Getting directories paths ...")
# Dataset and directories paths
dataset_path = 'MangoLeavesDatabase'
directories = [
    os.path.join(dataset_path, 'alphonso'),
    os.path.join(dataset_path, 'langra'),
    os.path.join(dataset_path, 'chausa'),
    os.path.join(dataset_path, 'amrapali'),
    os.path.join(dataset_path, 'dusheri'),
]
# Output path
output_path = os.path.join(dataset_path, 'output')
print("Processing Images ...")
# Start processing images
for dir in directories:
    dir_name = os.path.basename(dir)
    # Get all jpg image files within directory
    image_files = get_file_paths(dir, extension=['.jpg'], recursive=True)
    for image_file in image_files:
        img = Image.open(image_file)
        contrast = ImageEnhance.Contrast(img)
        contrasted_image = contrast.enhance(CONTRAST)
        brightness = ImageEnhance.Brightness(contrasted_image)
        bright_contrasted_img = brightness.enhance(BRIGHTNESS)
        sharpness = ImageEnhance.Sharpness(bright_contrasted_img)
        sharp_bright_contrasted_img = sharpness.enhance(SHARPNESS)
        color = ImageEnhance.Color(sharp_bright_contrasted_img)
        colored_sharp_bright_contrasted_img = color.enhance(COLOR)
        img_file_name = os.path.basename(image_file)
        _ , ext = img_file_name.split('.')
        filename = dir_name
        # Output Path
        out_file_path = os.path.join(output_path, dir_name)
        if 'front' in img_file_name:
            out_file_path = os.path.join(out_file_path, 'front')
            filename += '_front_'
        elif 'back' in img_file_name:
            out_file_path = os.path.join(out_file_path, 'back')
            filename += '_back_'
        # Make output path in filesystem
        if not os.path.exists(out_file_path):
            os.makedirs(out_file_path, exist_ok=True)
        # Original Image file name for output
        o_filename = filename + ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))
        o_out_file_name = o_filename + "." + ext
        # Enhanced Image file name for output
        en_filename = filename + ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))
        en_out_file_name = en_filename + "." + ext
        # Save Enhanced Image
        colored_sharp_bright_contrasted_img.save(os.path.join(out_file_path, en_out_file_name))
        if OUT_BOTH:
            # Save Original Image
            img.save(os.path.join(out_file_path, o_out_file_name))

print("Completed! Successfully enhanced dataset.")