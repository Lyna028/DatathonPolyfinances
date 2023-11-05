import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from tqdm import tqdm
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
marketCapData = filterYears(marketCapDefaultData)
ajustedCloseData = filterYears(ajustedCloseDefaultData)
normaliseAjustedCloseData = normalize_data(ajustedCloseData)

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

def averageMarketCap(currentDay, durationDays, company) :
    indexDay = marketCapData[volumeData['date'] == currentDay].index
    filtredMerketCap = marketCapData.iloc[indexDay[0]: indexDay[0] + durationDays]
    marketCapSum = filtredMerketCap[company].sum()
    #return marketCapSum/durationDays
    return filtredMerketCap

def long_terme_return( action, currentDay, durationDays):
    indexDay = normaliseAjustedCloseData[normaliseAjustedCloseData['timestamp'] == currentDay].index
    print(normaliseAjustedCloseData.loc[indexDay[0], action])
    print(normaliseAjustedCloseData.loc[indexDay[0]+durationDays, action])
    return normaliseAjustedCloseData.loc[indexDay[0], action] - normaliseAjustedCloseData.loc[indexDay[0]+durationDays, action]

#def finalFilter(currentDay, durationDays) :


print(averageMarketCap('2009-08-20', 4, 'volume_CSCO'))

