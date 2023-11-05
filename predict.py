import os
import math
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
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from filter import createXbySector
from filter import createYbySector

X = createXbySector('Health Care', '2007-11-09')
Y = createYbySector('Health Care', '2007-11-09')

nan_index = []
for index, value in enumerate(Y):
    if math.isnan(value):
        nan_index.append(index)
myY = [value for index, value in enumerate(Y) if index not in nan_index]
myX = [value for index, value in enumerate(X) if index not in nan_index]

X_train, X_test, y_train, y_test = train_test_split(myX, myY, test_size= 0.7, random_state=37)

regr = RandomForestRegressor(max_depth=12, random_state=17)
regr.fit(X_train, y_train)

y_pred = regr.predict(X_test)
y_real = y_test

df= pd.DataFrame({'Actual': y_real, 'Predicted': y_pred})
print(df)


print(regr.feature_importances_)

print(r2_score(y_real, y_pred))
print(mean_squared_error(y_real, y_pred))
print(mean_absolute_error(y_real, y_pred))
