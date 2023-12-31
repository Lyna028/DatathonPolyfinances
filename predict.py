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
from filter import getTreeX
from filter import symbolInfo

def getPredictOnDate(day):
    print('TEST')
    listStock = list()
    listSector = list()
    listReturn = list()
    sectorList = list()
    k = 5
    if day == '2000-01-03' : 
        k = 0
    elif day == '2000-08-07' :
        k = 3
    for stock in symbolInfo["Symbol"]:
        indexStock = symbolInfo[symbolInfo['Symbol'] == stock].index
        if symbolInfo.at[indexStock[0], 'GICS Sector'] not in sectorList:
            sectorList.append(symbolInfo.at[indexStock[0], 'GICS Sector'])
    for sector in sectorList :
        if True:
            X = createXbySector(sector, day, k)
            Y = createYbySector(sector, day, k)
            nan_index = []
            for index, value in enumerate(Y):
                if math.isnan(value):
                    nan_index.append(index)
            for index, value in enumerate(X) :
                for index_, value_ in enumerate(value):
                    if math.isnan(value_) and index_ not in nan_index:
                        nan_index.append(index_)
                        
            myY = [value for index, value in enumerate(Y) if index not in nan_index]
            myX = [value for index, value in enumerate(X) if index not in nan_index]

            X_train, X_test, y_train, y_test = train_test_split(myX, myY, test_size= 0.8, random_state=37)
            y_trainN = list()
            X_trainN = list()
            for i, s in zip(X_train, y_train):
                hasNan = False
                if math.isnan(s): hasNan = True
                for j in i:
                    if math.isnan(j):
                        hasNan = True
                if not hasNan : 
                    y_trainN.append(s)
                    X_trainN.append(i)


            regr = RandomForestRegressor(max_depth=11, random_state=17)

            regr.fit(X_trainN, y_trainN)
            for stock in symbolInfo["Symbol"]:
                indexStock = symbolInfo[symbolInfo['Symbol'] == stock].index
                if symbolInfo.at[indexStock[0], 'GICS Sector'] == sector:
                    x = getTreeX(day, stock)
                    xNan = False
                    for elem in x:
                        if math.isnan(elem):
                            xNan = True
                    if not xNan:
                        y_preds = regr.predict(np.array([getTreeX(day, stock)]))
                        listReturn.append(y_preds[0])
                        listStock.append(stock)
                        listSector.append(sector)
    normalized_Return = [(x - np.mean(listReturn)) / np.std(listReturn) for x in listReturn]
    df = pd.DataFrame({'Stock' : listStock, 'Sector' : listSector, 'Return' : normalized_Return})
    print(df)
    return df


        

# getPredictOnDate('2007-11-09')
