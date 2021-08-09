import lazypredict
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

#Read data file

import pandas as pd

filepath = "dataset/master-2.csv"
df = pd.read_csv(filepath)
features = df

# Labels are the values we want to predict
labels = np.array(df['protection_status'])

# Remove the labels from the features
features = features.drop('protection_status', axis = 1)
features = features.drop('page_title', axis = 1)
features = features.drop('page_id', axis=1)
features = features.drop('page_id_scrapped', axis=1)

#Convert String to Floats
features['page_length'] = features['page_length'].astype(float)
features['edit_count'] = features['edit_count'].astype(float)
features['page_watchers'] = features['page_watchers'].astype(float)
features['page_watchers_recent_edits'] = features['page_watchers_recent_edits'].astype(float)

# Saving feature names for later use
feature_list = list(features.columns)

# Convert to numpy array
features = np.array(features)

#Label encoding for protection_status column

# 0 => unprotected
# 1 => autoconfirmed
# 2 => extendedconfirmed
# 3 => sysop
labels_encoded = []
for item in labels:
    if(item =="unprotected"):
        labels_encoded.append(0)
    elif(item == "autoconfirmed"):
        labels_encoded.append(1)
    elif(item == "extendedconfirmed"):
        labels_encoded.append(2)
    elif(item == "sysop"):
        labels_encoded.append(3)  

# Using Skicit-learn to split data into training and testing sets
from sklearn.model_selection import train_test_split
# Split the data into training and testing sets
train_features, test_features, train_labels, test_labels = train_test_split(features, labels_encoded, test_size =0.20, random_state = 53)

X_train = train_features
y_train = train_labels
X_test = test_features
y_test = test_labels
from lazypredict.Supervised import LazyClassifier
clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
models,predictions = clf.fit(X_train, X_test, y_train, y_test)

print(models) 