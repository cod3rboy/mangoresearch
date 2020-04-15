import numpy as np
import pywt
import cv2
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize

def extract_haar_features(image_path, level=5, decompositions=['LL']):
    """
    This function extracts the haar features from an image at a given path and return those features as a tuple.
    
    arguments:
     image_path - string containing path to leaf image file.
     level (optional) - level up to which decomposition using haar wavelet must be performed.
     decompositions (optional) - decompositions to use at each level for generation of feature vectors. No of features = len(decompositions) * level. 
                                 This must me a list of any of the values 'LL', 'LH', 'HL' and 'HH'.
    returns:
     tuple object containing extracted features of the leaf.
    """
    # Read image from image file into grayscale mode. 
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if level <= 0 or level > 6:
        raise Exception("arg `level` must be >= 1 and <= 6")
    if decompositions is not None and type(decompositions) == list and len(decompositions) > 0:
        decompositions = list(map(str.lower, decompositions))
    else:
        raise Exception("arg `decompositions` must be a non-empty list of any of the values 'LL', 'LH', 'HL', 'HH'.")

    input = image
    decomposition_list = list()
    for i in range(level):
        LL, (LH, HL, HH) = pywt.dwt2(input, 'haar')
        for feature in decompositions:
            if   'll' == feature:
                decomposition_list.append(LL)
            elif 'lh' == feature:
                decomposition_list.append(LH)
            elif 'hl' == feature:
                decomposition_list.append(HL)
            elif 'hh' == feature:
                decomposition_list.append(HH)
        input = LL
    # Obtain histograms for all decompositions
    decomposition_histograms = list()
    for decomposition in decomposition_list:
        histogram, _ = np.histogram(np.ravel(decomposition), 256)
        decomposition_histograms.append(histogram)

    # Concatenate all histograms to get matrix of size n x 256 where n is no of extracted decompositions
    concat_hist = np.stack(decomposition_histograms, axis=0)

    # Apply Principle Component Analysis (PCA) for dimensionality reduction of n x 256 histogram matrix into n x 1 feature vector
    pca = PCA(n_components=1)
    feature_vector = np.ravel(pca.fit_transform(concat_hist))
    return feature_vector