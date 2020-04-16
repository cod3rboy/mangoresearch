### Feature Extraction and CSV Generation Script ###
# This script is used to extract haar features from the mango leaves dataset and generate a CSV file for training the classification model.
import pandas as pd
import numpy as np
import os
import utils
from features import extract_haar_features

# Prepare dataset directories and image files paths
# Leaves Dataset Folder Name
dataset = 'MangoLeavesDatabase'
# Get Current Working directory
working_dir = os.getcwd()
# Generate paths for varieties
paths = {
    'alphonso': os.path.join(working_dir, dataset, 'alphonso'),
    'amrapali': os.path.join(working_dir, dataset, 'amrapali'),
    'chausa': os.path.join(working_dir, dataset, 'chausa'),
    'dusheri': os.path.join(working_dir, dataset, 'dusheri'),
    'langra': os.path.join(working_dir, dataset, 'langra'),
}
# Generate a dictionary storing lists of image paths of a particular variety accessible using corresponding variety name. 
image_dict = dict()
for label, path in paths.items():
    image_dict[label] = utils.get_file_paths(path, ['.jpg'])
# CSV file output path
csv_file_output_path = os.path.join(working_dir, dataset, 'labeled_haar_dataset.csv')

# Generate Pandas DataFrame containing extracted features for each image file. 
# If M features are extracted from N images then DataFrame will be of N x M dimension.
## Generate Columns List for the data
LEVEL = 5
DECOMPOSITIONS = ['LL', 'HL', 'LH']
cols = [DECOMPOSITIONS[y] + str(x)
        for x in range(1, LEVEL + 1)
        for y in range(len(DECOMPOSITIONS))]
cols.append("Label")

# Create an empty dataframe with above columns
data = pd.DataFrame(columns=cols)
row_list = list()
# Extract image features of each image of each variety
for label, path_list in image_dict.items():
    for image_path in path_list:
        features = extract_haar_features(image_path, level=LEVEL, decompositions=DECOMPOSITIONS)
        data_row = np.concatenate((features, [label]), axis=0)
        row_dict = dict()
        for i in range(len(cols)):
            row_dict[cols[i]] = data_row[i]
        row_list.append(row_dict)

data = data.append(row_list, ignore_index=True)

# Shuffle the rows of data before saving
data = data.sample(frac=1).reset_index(drop=True)
# Save data to CSV file
data.to_csv(csv_file_output_path)
print("Successfully generated CSV file at path " + csv_file_output_path)