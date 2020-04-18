# This script is used to highlight leaf contour in each image of the dataset and export the resulted image in output directory.
import cv2
import os
import time
import numpy as np
from utils import get_file_paths

# Prepare dataset directories
print("Prepare dataset directories ...")
DATASET_DIR = os.path.join(os.getcwd(), 'MangoLeavesDatabase')
VARIETY_DIRS = [
    'alphonso',
    'amrapali',
    'chausa',
    'dusheri',
    'langra',
]
OUTPUT_DIRECTORY = os.path.join(DATASET_DIR, 'contour_output')

ts = time.time()
print("Processing Images ...")
for variety in VARIETY_DIRS:
    image_paths = get_file_paths(os.path.join(DATASET_DIR, variety), extension=['.jpg'], recursive=True)
    for img_path in image_paths:
        # Read an Image from dataset
        original_img = cv2.imread(img_path)
        # Image File Name 
        img_file_name = os.path.basename(img_path)
        # Convert color channels from BGR to RGB
        img2rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        # Apply K-Means to reduce color space in image
        img_pixels = np.float32(img2rgb.reshape((-1, 3)))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 5 # no of clusters
        ret,labels,centers = cv2.kmeans(img_pixels, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        cluster_img = centers[labels.flatten()]
        # Change all non-green pixels to white in clustered image
        for i,p in enumerate(cluster_img):
            if p[1] < p[0] or p[1] < p[2]:
                cluster_img[i] = [255, 255, 255]
        cluster_img = cluster_img.reshape(img2rgb.shape)
        # Apply thresholding to clustered image
        cluster_img2gray = cv2.cvtColor(cluster_img, cv2.COLOR_RGB2GRAY)
        retval, th_img = cv2.threshold(cluster_img2gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        # Find contours in threshold image
        contours, _ = cv2.findContours(th_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            # Get contour with largest area as leaf contour
            leaf_contour = max(contours, key=cv2.contourArea)
            # Get the bounding box for leaf contour
            x, y, w, h = cv2.boundingRect(leaf_contour)
            # Draw contours on original, clustered and threashold images
            out_img = cv2.drawContours(img2rgb, [leaf_contour], 0, (255,0,0), 1)
            out_img = cv2.cvtColor(out_img, cv2.COLOR_RGB2BGR) # OpenCV saves images in BGR Channel Mode.
            out_path = os.path.join(OUTPUT_DIRECTORY, variety)
            os.makedirs(out_path, exist_ok=True)
            status = cv2.imwrite(os.path.join(out_path, img_file_name), out_img)
            print("Contour found in image : " + img_file_name)
        else:
            print('No contour found in image : ' + img_file_name)

te = time.time()
# Compute Time Elapsed
HOUR_SECS = 60 * 60
MIN_SECS = 60
seconds = int(te - ts)
hours = seconds // HOUR_SECS
seconds = seconds % HOUR_SECS
mins = seconds // MIN_SECS
seconds = seconds % MIN_SECS
s = "TIME ELPASED : "
if hours > 0:
    s += str(hours) + " Hours "
if mins > 0:
    s += str(mins) + " Mins "
if seconds > 0:
    s += str(seconds) + " Secs "

print("Completed! Output can be found at path " + OUTPUT_DIRECTORY)
print(s)