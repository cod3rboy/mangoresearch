import numpy as np
import pywt
import cv2
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize

def extract_haar_features(image_path, decomposition_level=5, alternate_feature='hl'):
    """
    This function extracts the haar features from an image at a given path and return those features as a tuple.
    
    arguments:
     image_path - string containing path to leaf image file.
     decomposition_level (optional) - level up to which decomposition using haar wavelet must be performed.
     alternate_feature (optional) - second decomposition to be used to compute additional features.
    returns:
     tuple object containing extracted features of the leaf.
    """
    # Read image from image file into grayscale mode. 
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if decomposition_level <= 0 or decomposition_level > 6:
        raise Exception("Decomposition Level must be >= 1 and <= 6")
    if alternate_feature is not None and not alternate_feature.lower() in ['hl', 'lh', 'hh']:
        raise Exception("Alternate feature must be one of the values 'LH', 'HL', 'HH' or None.")
    input = image
    decomposition_list = list()
    for i in range(decomposition_level):
        LL, (LH, HL, HH) = pywt.dwt2(input, 'haar')
        decomposition_list.append(LL)
        if alternate_feature is not None:
            alternate_feature = alternate_feature.lower()
            if alternate_feature == 'lh':
                decomposition_list.append(LH)
            elif alternate_feature == 'hl':
                decomposition_list.append(HL)
            elif alternate_feature == 'hh':
                decomposition_list.append(HH)
        input = LL
    
    # Obtain histograms for all decompositions
    decomposition_histograms = list()
    for decomposition in decomposition_list:
        histogram, _ = np.histogram(np.ravel(decomposition), 256, (0, 255))
        decomposition_histograms.append(histogram)

    # Concatenate all histograms to get matrix of size n x 256 where n is no of extracted decompositions
    concat_hist = np.stack(decomposition_histograms, axis=0)

    # Apply Principle Component Analysis (PCA) for dimensionality reduction of n x 256 histogram matrix into n x 1 feature vector
    pca = PCA(n_components=1)
    feature_vector = np.ravel(pca.fit_transform(concat_hist))
    return feature_vector
