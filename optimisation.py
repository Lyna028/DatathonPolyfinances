import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
# from tqdm import tqdm
from sklearn.preprocessing import StandardScaler

from predict import getPredictOnDate

path = os.getcwd()
submissionDf = pd.read_csv(os.path.join(path, 'series/submission.csv'))
submissionDfResult = pd.read_csv('series/submissionResult.csv')


def optimizeWallet(day) : 
    df = getPredictOnDate(day)
    sorted_df = df.sort_values(by='Return', ascending=False)
    top_sorted = sorted_df.head(130)
    bySectionWeight = {
        'Industrials' : [0,0],
        'Health Care' : [0,0],
        'Information Technology' : [0,0],
        'Consumer Staples' : [0,0],
        'Utilities' : [0,0],
        'Financials' : [0,0],
        'Materials' : [0,0],
        'Communication Services' : [0,0],
        'Consumer Discretionary' : [0,0],
        'Real Estate' : [0,0],
        'Energy' : [0,0]
    }
    totalReturn = 0
    for index, row in top_sorted.iterrows() :
        sector = row['Sector']
        value = row['Return']
        bySectionWeight[sector][0] += value
        totalReturn += value
    perSectPercent = {}
    for index, row in top_sorted.iterrows() :
        stock = row['Stock']
        sector = row['Sector']
        value = row['Return']
        perSectPercent[stock] = value/bySectionWeight[sector][0]

    for key, value in bySectionWeight.items() :
        value[1] = value[0] / totalReturn

    for key, value in bySectionWeight.items() :
        if value[0]/totalReturn < 0.05:
            max_key = max(bySectionWeight, key=lambda key: bySectionWeight[key][0])
            valueToGive = 0.05 - value[1]
            bySectionWeight[max_key][0] -= valueToGive*totalReturn
            bySectionWeight[max_key][1] -= valueToGive
            bySectionWeight[key][0] = totalReturn * 0.05
            bySectionWeight[key][1] = 0.05
    myOptimizedWallet = {}
    for index, row in top_sorted.iterrows() :
        sector = row['Sector']
        stock = row['Stock']
        value = row['Return']
        myOptimizedWallet[stock] = perSectPercent[stock] * bySectionWeight[sector][1]

    mySum = 0
    return myOptimizedWallet

dfSubmit = pd.DataFrame(submissionDf)
print(dfSubmit)
for i in range(0, 150, 150) : ### 3772
    indexDate = dfSubmit[dfSubmit['id'] == i].index
    date = dfSubmit.at[indexDate[0], 'date']
    myWallet = optimizeWallet(date)
    for column in dfSubmit.columns :
        if column == 'id':
            continue
        elif column == 'date':
            continue
        else:
            isInWallet = False
            value_ = 0
            for key, value in myWallet.items() :
                if column == 'weight_' + key :
                    isInWallet = True
                    value_ = abs(value)
            for j in range(i, i+149, 1) :
                dfSubmit.at[j, column] = value_
print(dfSubmit)
dfSubmit.to_csv('series/submissionResult.csv')

            






