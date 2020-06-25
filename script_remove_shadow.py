# Python script to remove shadows and isolate leaf portion in dataset images
from utils import get_file_paths
import numpy as np
import cv2
import os

def remove_shadow_and_isolate(image_path, k):
    # Read an Image from dataset
    original_img = cv2.imread(image_path)
    # Convert color channels from BGR to RGB
    img2rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    # Apply K-Means to reduce color space in image
    img_pixels = np.float32(img2rgb.reshape((-1, 3)))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, k, 1.0)
    K = k # no of clusters
    ret,labels,centers = cv2.kmeans(img_pixels, K, None, criteria, k, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    cluster_img = centers[labels.flatten()]
    # Set shadow bluish pixels to white
    for i,p in enumerate(cluster_img):
        max_intensity = max(p)
        if max_intensity == p[2]:
            cluster_img[i] = [255, 255, 255]
    cluster_img = cluster_img.reshape(img2rgb.shape)
    # Apply Morphological opening
    # kernel = np.ones((5,5), np.uint8)
    # opening = cv2.morphologyEx(cluster_img, cv2.MORPH_CLOSE, kernel)
    # Apply thresholding to clustered opening image
    cluster_img2gray = cv2.cvtColor(cluster_img, cv2.COLOR_RGB2GRAY)
    retval, th_img = cv2.threshold(cluster_img2gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


src_path = input("Enter source dataset path : ")
image_file_paths = get_file_paths(src_path, extension=['.jpg'], recursive=True)
total_images = len(image_file_paths)
print("Total Images : " + str(total_images))
print("Removing shadows and isolating leaf in images :-")
i=0
for img_path in image_file_paths:
    filename, ext = os.path.basename(img_path).split(".")
    dirname = os.path.dirname(img_path)
    save_path = os.path.join(dirname, filename + "_p." + ext)
    img = remove_shadow_and_isolate(img_path, 10)
    cv2.imwrite(save_path, img)
    i += 1
    print(str(i) + "/" + str(total_images) + " processed.")
print("Completed!")