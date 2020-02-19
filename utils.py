import os
from PIL import Image


def get_file_paths(dir_name, extension=None, recursive=True):
    """
    For the given path, get the list of all filepath suffixed with given extension in the directory tree.
    If extension is None then it includes any file.
    :param dir_name: Name of directory to search in
    :param extension: To include files matching this extension
    :param recursive: When to search in subdirectories
    :return: List of all included file paths
    """
    dir_filenames = os.listdir(dir_name)  # All filenames in the directory
    file_path_list = list()  # List of filenames to return
    # Iterate over all the entries
    for entry in dir_filenames:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path) and recursive:
            # Recursively call this function on directories and append the results to the results of this function.
            file_path_list = file_path_list + get_file_paths(full_path, extension)
        else:
            if extension is None or len(extension) == 0:
                # Only append file if either extension is not provided or filename ends with given extension.
                file_path_list.append(full_path)
            else:
                for ext in extension:
                    if full_path.lower().endswith(ext):
                        file_path_list.append(full_path)
                        break

    return file_path_list


def rotate_image(image_path, deg, save_location):
    """
    Rotates an image at path at a specified degree and saves it to the given save location.
    :param image_path: Path of the image to rotate
    :param deg: angle at which to rotate the image
    :param save_location: path at which rotated image will be saved
    :return: None
    """
    img = Image.open(image_path)
    img_rotated = img.rotate(deg, expand=True)  # expand=True will change image size to fit the rotated image
    img_rotated.save(save_location)
