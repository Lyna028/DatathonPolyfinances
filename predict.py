import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
# from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from filter import createXbySector
from filter import createYbySector


# myX = ((1, 3, 4), (4, 5, 7), (8, 11, 3), (4, 2, 5), (6, 5, 4), (1, 1, 6))
# myY = (3.5, 6, 5, 3, 4.5, 3)
# # myY = (2, 4, 7, 3, 6, 2)

# equipement_data = pd.read_csv('series/trainingData/Equipement-1.csv', delimiter=';', decimal=",")
# equipement_data['Y'] = equipement_data['Y'].map({'D': 1, 'N': 0})

# myX = equipement_data[['X1', 'X2']]
# myY = equipement_data['Y']

myX = createXbySector('Health Care', '2013-11-05')
myY = createYbySector('Health Care', '2013-11-05')
print(myX)

# myX, myY = make_classification(n_samples=len(myX), n_features=8, n_redundant=0, random_state=42, shuffle= False)
myX, myY = make_regression( n_features=8, random_state=42, shuffle= False)


X_train, X_test, y_train, y_test = train_test_split(myX, myY, test_size= 0.7, random_state=52)


regr = RandomForestRegressor(max_depth=4, random_state=42)
regr.fit(X_train, y_train)

y_pred = regr.predict(X_test)
y_real = y_test

print(y_pred)

df= pd.DataFrame({'Actual': y_real, 'Predicted': y_pred})
print(df)

def getAverageSuccess(df):
    sumSuccess = 0
    for i, j in zip(df['Actual'], df['Predicted']):
        sumSuccess += i/j
        print(i/j)
    return sumSuccess/33
print(getAverageSuccess(df))