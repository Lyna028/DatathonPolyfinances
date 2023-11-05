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
# marketCapData = filterYears(marketCapDefaultData)
ajustedCloseData = filterYears(ajustedCloseDefaultData)
normaliseAjustedCloseData = normalize_data(ajustedCloseData)

## CA MARCHE
def averageVolume(currentDay, durationDays, company) :
    indexDay = volumeData[volumeData['timestamp'] == currentDay].index
    filtredVolume = volumeData.iloc[indexDay[0] : indexDay[0] + durationDays]
    volumSum = filtredVolume['volume_' + company].sum()
    return volumSum/durationDays

# def averageMarketCap(currentDay, durationDays, company) :
#     indexDay = marketCapData[volumeData['date'] == currentDay].index
#     filtredMerketCap = marketCapData.iloc[indexDay[0]: indexDay[0] + durationDays]
#     marketCapSum = filtredMerketCap[company].sum()
#     #return marketCapSum/durationDays
#     return filtredMerketCap

# CA MARCHE
def long_terme_return(currentDay, durationDays, stock):
    indexDay = normaliseAjustedCloseData[normaliseAjustedCloseData['timestamp'] == currentDay].index
    return normaliseAjustedCloseData.loc[indexDay[0], stock] - normaliseAjustedCloseData.loc[indexDay[0]+durationDays, 'adjusted_close_' + stock]

def getReturnByDay(entry, close):
    return (close-entry)/entry * 100

def getReturnTable(dayOne, nDay, company):
    returnTable = list()
    openIndex = openData[openData['timestamp'] == dayOne].index
    openTable = openData.iloc[openIndex[0] : openIndex[0] + nDay]
    closeIndex = closeData[closeData['timestamp'] == dayOne].index
    closeTable = closeData.iloc[closeIndex[0] : closeIndex[0] + nDay]
    for i, j in zip(closeTable['close_' + company], openTable['open_' + company]) :
        returnTable.append(getReturnByDay(j, i))
    return returnTable

##CA MARCHE
def gapValue (startDate, duration, company):
    indexDay = normaliseAjustedCloseData[ajustedCloseData['timestamp'] == startDate].index
    filteredAjustedCloseData = normaliseAjustedCloseData.iloc[indexDay[0] : indexDay[0] + duration]
    selectionnedDataCompany = filteredAjustedCloseData['adjusted_close_' + company]
    valMax = selectionnedDataCompany.max()
    valMin = selectionnedDataCompany.min()
    gapValue = valMax-valMin
    return gapValue

def getCloseLowHigh(dayOne, nDay, company):
    closeIndex = closeData[closeData['timestamp'] == dayOne].index
    closeTable = closeData.iloc[closeIndex[0] : closeIndex[0] + nDay]
    selectionnedDataCompany = closeTable['close_' + company]
    print(closeTable.min())
    return (closeTable.min(), closeTable.max())

print(closeData)
print(getCloseLowHigh('2014-12-31', 4, 'CSCO'))
def getReturnAverage(stock, dayOne, nDay):
    myList = getReturnTable(dayOne, nDay, stock)
    sumReturn = 0
    for i in myList:
        sumReturn += i
    return sumReturn/nDay

def getReturnGap(stock, dayOne, nDay):
    myList = getReturnTable(dayOne, nDay, stock)
    return max(myList) - min(myList)

def getPositiveReturn(stock, currentDay, durationDays):
    nPositiveDays = 0
    table = getReturnTable(currentDay, durationDays, stock)
    for i in table:
        nPositiveDays += 1 if i > 0 else 0

    return nPositiveDays/durationDays*100

# def getTreeY(day, company):
    # indexDay = normaliseAjustedCloseData[normaliseAjustedCloseData['timestamp'] == day].index
    # return normaliseAjustedCloseData.loc[indexDay[0]-day, company] - normaliseAjustedCloseData.loc[indexDay[0], company] 

## la suivante existe en attendant que le normalise fonctionne
def getTreeY(day, company, nDay):
    indexDay = closeData[closeData['timestamp'] == day].index
    return closeData.loc[indexDay[0]-nDay, 'close_' + company] - closeData.loc[indexDay[0], 'close_' + company] 
