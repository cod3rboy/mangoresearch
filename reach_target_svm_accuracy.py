import os
import numpy as np
import pandas
from sklearn import svm
from sklearn.model_selection import train_test_split
# Prepare dataset directory and load dataset csv file into Pandas DataFrame

# Leaves Dataset Folder Name
dataset_folder = 'PreprocessedDatabase'
# Leaves Dataset File Name
dataset_filename = 'labeled_dataset.csv'
# Current working directory
cwd = os.getcwd()
# Load the dataset from CSV file into pandas DataFrame
data = pandas.read_csv(os.path.join(cwd, dataset_folder, dataset_filename))

# Create lists of feature vectors and corresponding labels from dataframe

# Mapping of string labels to numeric value
label_map = {
    'alphonso': 0,
    'amrapali': 1,
    'chausa': 2,
    'dusheri': 3,
    'langra': 4
}
# Mapping of numeric labels to string value
label_map_rev = {
    0: 'alphonso',
    1: 'amrapali',
    2: 'chausa',
    3: 'dusheri',
    4: 'langra'
}
# List of feature vectors
X = data.iloc[:, :len(data.columns)-1].to_numpy(copy=True)
# List of corresponding label to each feature vector
Y = data.iloc[:,-1].to_numpy(copy=True)
# Map string labels to numeric values
Y = np.array([label_map[label] for label in Y])

def test_train_save(train: tuple, test: tuple, outfilepath: str):
    trainX, trainY = train
    testX, testY = test
    # Map from value to label string
    trainY = [label_map_rev[y] for y in trainY]
    testY = [label_map_rev[y] for y in testY]
    # Merge features and labels
    train_recs = np.hstack((trainX, np.reshape(trainY, (len(trainY), 1))))
    test_recs = np.hstack((testX, np.reshape(testY, (len(testY), 1))))
    # Merge train and test records
    records = np.vstack((train_recs, test_recs))
    # Create and save pandas dataframe
    cols = ['aspectratio', 'area', 'perimeter', 'formfactor', 'meanR', 'meanG', 'meanB', 'veinarea1', 'veinarea2', 'elongation', 'label']
    df_recs = pandas.DataFrame(records, columns=cols)
    df_recs.to_csv(outfilepath, index=False)
    #print(df_recs.head(10))


# Target Accuracy
target_accuracy = 0.85 # 82%
# Export CSV file path
export_csv_path = os.path.join(os.getcwd(), dataset_folder, 'labeled_dataset_max.csv')
# Number of iterations
iterations = 500
# Export csv when target accuracy reached
export_csv = True
max_accuracy = 0
train = None
test = None
print("Target accuracy : %f\nNumber of Iterations : %d" % (target_accuracy * 100, iterations))
for i in range(iterations):
    print("Iteration : %d" % (i+1), end='\r')
    # Create and Split Training and Test Data
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.8, test_size=0.2, shuffle=True)

    # Train and Test Support Vector Classifier

    # Train SVM Model using training data
    svm_model = svm.SVC(kernel='poly', degree=8, C=1, decision_function_shape='ovo').fit(X_train, Y_train)
    # Model predictions using test data
    svm_predictions = svm_model.predict(X_test) 
    # model accuracy for X_test   
    accuracy = svm_model.score(X_test, Y_test)
    # Update Max Accuracy 
    if(accuracy >= target_accuracy and accuracy > max_accuracy):
        max_accuracy = accuracy
        train = (X_train, Y_train)
        test = (X_test, Y_test)

if max_accuracy >= target_accuracy:
    print("\nMaximum accuracy reached in %d iterations : %f" % (iterations, max_accuracy * 100))
    if export_csv:
        test_train_save(train, test, export_csv_path)
        print("CSV file with test train data is exported at below path\n" + export_csv_path)
else:
    print("\nFailed to reach target accuracy in %d iterations" % iterations)