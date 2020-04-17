# This Script is used to reduce the size of enhanced dataset images by a factor of 3.
import os
from PIL import Image
from utils import get_file_paths

# Scale by which to reduce each dimension of image
REDUCE_SCALE = 3

# Dataset Directory Name
dataset_dir_name = 'MangoLeavesDatabase'

# Retrieve all image paths in the dataset directory
image_files = get_file_paths(os.path.join(os.getcwd(), dataset_dir_name), extension=['.jpg'], recursive=True)
print("Resizing images ...")
for img_file in image_files:
    # Read Image
    img = Image.open(img_file)
    # Get original width and height
    w, h = img.size
    # Resize the image by applying REDUCE_SCALE in both dimensions
    resized_img = img.resize((w // REDUCE_SCALE, h // REDUCE_SCALE), Image.ANTIALIAS)
    # Save resized image by overwriting original image.
    resized_img.save(img_file, 'JPEG')
print("Resizing Completed!")

