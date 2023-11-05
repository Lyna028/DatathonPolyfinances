import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
# from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# myX = ((1, 3, 4), (4, 5, 7), (8, 11, 3), (4, 2, 5), (6, 5, 4), (1, 1, 6))
# myY = (3.5, 6, 5, 3, 4.5, 3)
# # myY = (2, 4, 7, 3, 6, 2)

equipement_data = pd.read_csv('series/trainingData/Equipement-1.csv', delimiter=';', decimal=",")
equipement_data['Y'] = equipement_data['Y'].map({'D': 1, 'N': 0})

myX = equipement_data[['X1', 'X2']]
myY = equipement_data['Y']


myX, myY = make_classification(n_samples=299, n_features=2, n_redundant=0, random_state=42, shuffle= False)
X_train, X_test, y_train, y_test = train_test_split(myX, myY, test_size= 100, random_state=42)


clf = RandomForestClassifier(max_depth=4, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
y_real = y_test

df= pd.DataFrame({'Actual': y_real, 'Predicted': y_pred})

def getAverageSuccess(df):
    sumSuccess = 0
    for i, j in zip(df['Actual'], df['Predicted']):
        if(i == j): sumSuccess += 1
    return sumSuccess/100
print(getAverageSuccess(df))