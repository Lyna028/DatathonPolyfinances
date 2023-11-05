import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
# from tqdm import tqdm
from sklearn.preprocessing import StandardScaler

path = os.getcwd()
volumeDefaultData = pd.read_csv(os.path.join(path, 'series/volume.csv'))
openDefaultData = pd.read_csv(os.path.join(path, 'series/open.csv'))
highDefaultData = pd.read_csv(os.path.join(path, 'series/high.csv'))
closeDefaultData = pd.read_csv(os.path.join(path, 'series/close.csv'))
lowDefaultData = pd.read_csv(os.path.join(path, 'series/low.csv'))
marketCapDefaultData = pd.read_csv(os.path.join(path, 'series/additional_data/market_cap.csv'))
ajustedCloseDefaultData = pd.read_csv(os.path.join(path, 'series/adjusted_close.csv'))

def filterYears(data) :
    if 'timestamp' in
    filtered_data = data[(data['timestamp'] >= '2000-01-01') & (data['timestamp'] <= '2015-01-01')]
    return filtered_data.reset_index(drop=True)

def normalize_data(data):
    timestamps = data['timestamp']
    data = data.drop(columns=['timestamp'])
    standardized_data = pd.DataFrame(StandardScaler().fit_transform(data), columns=data.columns)
    standardized_data['timestamp'] = timestamps
    return standardized_data

volumeData = filterYears(volumeDefaultData)
openData = filterYears(openDefaultData)
highData = filterYears(highDefaultData)
closeData = filterYears(closeDefaultData)
lowData = filterYears(lowDefaultData)
<<<<<<< Updated upstream
#marketCapData = filterYears(marketCapDefaultData)
=======
# marketCapData = filterYears(marketCapDefaultData)
>>>>>>> Stashed changes
ajustedCloseData = filterYears(ajustedCloseDefaultData)
# normaliseAjustedCloseData = normalize_data(ajustedCloseData)

def averageVolume(currentDay, durationDays, company) :
    indexDay = volumeData[volumeData['timestamp'] == currentDay].index
    filtredVolume = volumeData.iloc[indexDay[0] : indexDay[0] + durationDays]
    volumSum = filtredVolume[company].sum()
    return volumSum/durationDays

def ecartTypeValue ( startDate, duration,company):
    selectionnedDataIndex = ajustedCloseData[ajustedCloseData['timestamp'] == startDate].index
    selectionnedData = ajustedCloseData.iloc[selectionnedDataIndex[0] : selectionnedDataIndex[0] + duration +1]
    selectionnedDataCompany = selectionnedData[company]
    valMax = selectionnedDataCompany.max()
    valMin = selectionnedDataCompany.min()
    ecartTypeValue = valMax-valMin
    return ecartTypeValue

<<<<<<< Updated upstream
def averageMarketCap(currentDay, durationDays, company) :
    indexDay = marketCapDefaultData[marketCapDefaultData['date'] == currentDay].index
    filtredMarketCap = marketCapDefaultData.iloc[indexDay[0]: indexDay[0] + durationDays + 1]
    marketCapSum = filtredMarketCap[company].sum()
    #return marketCapSum/durationDays
    return filtredMarketCap

print(averageMarketCap('2018-10-31', 4, 'market_cap_CSCO'))
=======
# def averageMarketCap(currentDay, durationDays, company) :
#     indexDay = marketCapData[volumeData['date'] == currentDay].index
#     filtredMerketCap = marketCapData.iloc[indexDay[0]: indexDay[0] + durationDays]
#     marketCapSum = filtredMerketCap[company].sum()
#     #return marketCapSum/durationDays
#     return filtredMerketCap
>>>>>>> Stashed changes

def long_terme_return( action, currentDay, durationDays):
    indexDay = normaliseAjustedCloseData[normaliseAjustedCloseData['timestamp'] == currentDay].index
    print(normaliseAjustedCloseData.loc[indexDay[0], action])
    print(normaliseAjustedCloseData.loc[indexDay[0]+durationDays, action])
    return normaliseAjustedCloseData.loc[indexDay[0], action] - normaliseAjustedCloseData.loc[indexDay[0]+durationDays, action]

<<<<<<< Updated upstream
=======
#def finalFilter(currentDay, durationDays) :


# print(averageMarketCap('2009-08-20', 4, 'volume_CSCO'))


>>>>>>> Stashed changes
def getReturnByDay(entry, close):
    return (close-entry)/entry * 100

def getReturnTable(dayOne, nDay, company):
    returnTable = list()

    openIndex = openData[openData['timestamp'] == dayOne ].index
    openTable = openData.iloc[openIndex[0] : openIndex[0] + nDay + 1]

    closeIndex = closeData[closeData['timestamp'] == dayOne ].index
    closeTable = closeData.iloc[closeIndex[0] : closeIndex[0] + nDay + 1]

    for i, j in zip(closeTable['close_' + company], openTable['open_' + company]) :
        returnTable.append(getReturnByDay(j, i))
    return returnTable
<<<<<<< Updated upstream
=======

print(getReturnTable('2009-08-20', 7, 'CSCO'))

def getPositiveReturn(action, currentDay, durationDays):
    nPositiveDays = 0
    table = getReturnTable(currentDay, durationDays, action);
    for i in table:
        nPositiveDays += 1 if i > 0 else 0

    return nPositiveDays/durationDays*100

def getValueGap(dayOne, nDay, company):
    adjustedCloseIndex = ajustedCloseData[ajustedCloseData['timestamp'] == dayOne ].index
    adjustedCloseTable = ajustedCloseData.iloc[adjustedCloseIndex[0] : adjustedCloseIndex[0] + nDay + 1]
    closeList = 
    for i in adjustedCloseTable :


>>>>>>> Stashed changes
