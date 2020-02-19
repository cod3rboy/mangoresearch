import os
from utils import get_file_paths, rotate_image

"""
  ####  PYTHON SCRIPT ####
  This script is used to help rotate images using Python Pillow library.
  Usage :- Create a directory named rotation and then create subdirectories with rotation angle name i.e. 90 or 180 or 270 ,etc.
  Put all the images inside the subdirectory with name of desired rotation angle.
  Run this script from the path whose the directory structure contain rotation directory.
  This script will apply desired rotation to all images inside all rotation directories present in the working directory structure.
"""

# Directory in which to place image files to rotate
dir_name = 'rotation'

# Map which determines the rotation degree using directory name
# thus images which need to rotate at 90 deg must inside a directory named 90 within the root directory rotation
rotation_dir_map = {
    "90": 90,
    "180": 180,
    "270": 270,
    "360": 360,
}

# List of supported image file types
supported_images = [
    '.jpg', '.jpeg', '.png', '.bmp',
]

# Get current working directory
working_dir = os.getcwd()

# To store paths of rotation directories found in the directory tree
rotation_dirs = list()

# List of directories in which we need to find rotation directory
dirs = [working_dir]  # start with working directory

while len(dirs) != 0:
    d = dirs.pop()  # Remove a directory
    entries = os.listdir(d)  # Get all the entries in directory
    for entry in entries:
        entry_path = os.path.join(d, entry)  # Make absolute entry path
        if os.path.isdir(entry_path):  # Check whether entry is a sub directory
            if entry.lower() == dir_name.lower():
                # Add if entry is a rotation directory
                rotation_dirs.append(entry_path)
            else:
                # If entry is not a rotation directory then add this directory to
                # the list of directories to process
                dirs.append(entry_path)


# Print all rotation directories found
print("Rotation directories found at following paths --")
for d in rotation_dirs:
    print(d)

# Start processing images in rotation directories
print("Starting image processing ... ")
for r_dir in rotation_dirs:
    # Try to find all supported sub directories named with rotation degree using rotation_dir_map
    for sub_dir_name, rotation_deg in rotation_dir_map.items():
        # Create sub directory path
        sub_dir_path = os.path.join(r_dir, sub_dir_name)
        if not os.path.exists(sub_dir_path):
            # Skip if sub directory not exists
            continue
        else:
            # Obtain all supported images with in sub directory
            image_paths = get_file_paths(sub_dir_path, supported_images, recursive=False)
            if len(image_paths) == 0:  # No image found in sub directory
                print('No image to process at path : ', sub_dir_path)
            else:
                # Rotate all images in sub directory at degree after which sub directory is named (rotation_deg).
                print("Rotating all images at path at %d deg:" % rotation_deg, sub_dir_path)
                for path in image_paths:
                    rotate_image(path, rotation_deg, path)
                    print("Rotated %d deg" % rotation_deg, os.path.basename(path))

print("Completed! All images are processed successfully.")
