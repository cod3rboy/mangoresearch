## Python Script to expand dataset by enhancing existing images in dataset.

import os
from PIL import Image, ImageEnhance
from utils import get_file_paths

# Image Enhancemnet Parameters
CONTRAST = 1.1 # 0 : No Contrast Gray Image and 1 : Original Image
BRIGHTNESS = 1.3 # 0 : No Brightness and  > 1 : More Brightness
SHARPNESS = 2.0 # 0 : Blurness , 1 : No Sharpness , > 1 : Sharp Image
COLOR = 1.5 # 0 : No Color (Grayscale), 1 : Original Color , > 1 Saturated Color

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
        filename, ext = img_file_name.split('.')
        # Original Image file name for output
        o_out_file_name = filename + "_0." + ext
        # Enhanced Image file name for output
        en_out_file_name = filename + "_1." + ext
        # Output Path
        out_file_path = os.path.join(output_path, dir_name)
        if 'front' in img_file_name:
            out_file_path = os.path.join(out_file_path, 'front')
        elif 'back' in img_file_name:
            out_file_path = os.path.join(out_file_path, 'back')
        # Make output path in filesystem
        if not os.path.exists(out_file_path):
            os.makedirs(out_file_path, exist_ok=True)
        # Save Enhanced Image
        colored_sharp_bright_contrasted_img.save(os.path.join(out_file_path, en_out_file_name))
        # Save Original Image
        img.save(os.path.join(out_file_path, o_out_file_name))

print("Completed! Successfully enhanced dataset.")