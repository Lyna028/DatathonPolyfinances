import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
# from tqdm import tqdm
# from sklearn.preprocessing import StandardScaler

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
# normaliseAjustedCloseData = normalize_data(ajustedCloseData)

def averageVolume(currentDay, durationDays, company) :
    indexDay = volumeData[volumeData['timestamp'] == currentDay].index
    filtredVolume = volumeData.iloc[indexDay[0] : indexDay[0] + durationDays]
    volumSum = filtredVolume[company].sum()
    return volumSum/durationDays

def gapValue ( startDate, duration,company):
    selectionnedDataIndex = ajustedCloseData[ajustedCloseData['timestamp'] == '2023-10-04'].index
    # selectionnedData = ajustedCloseData.iloc[selectionnedDataIndex[0] : selectionnedDataIndex[0] + duration +1]
    # selectionnedDataCompany = selectionnedData[company]
    # valMax = selectionnedDataCompany.max()
    # valMin = selectionnedDataCompany.min()
    # gapValue = valMax-valMin
    # return gapValue


# def averageMarketCap(currentDay, durationDays, company) :
#     indexDay = marketCapData[volumeData['date'] == currentDay].index
#     filtredMerketCap = marketCapData.iloc[indexDay[0]: indexDay[0] + durationDays]
#     marketCapSum = filtredMerketCap[company].sum()
#     #return marketCapSum/durationDays
#     return filtredMerketCap

def long_terme_return( stock, currentDay, durationDays):
    indexDay = normaliseAjustedCloseData[normaliseAjustedCloseData['timestamp'] == currentDay].index
    print(normaliseAjustedCloseData.loc[indexDay[0], stock])
    print(normaliseAjustedCloseData.loc[indexDay[0]+durationDays, stock])
    return normaliseAjustedCloseData.loc[indexDay[0], stock] - normaliseAjustedCloseData.loc[indexDay[0]+durationDays, stock]


#def finalFilter(currentDay, durationDays) :


# print(averageMarketCap('2009-08-20', 4, 'volume_CSCO'))

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

def getCloseLowHigh(company, dayOne, nDay):
    closeTable = list()

    closeIndex = closeData[closeData['timestamp'] == dayOne ].index
    closeTable = closeData.iloc[closeIndex[0] : closeIndex[0] + nDay + 1]

    for i in closeTable['close_' + company]:
        closeTable.append(i)
    return (min(closeTable), max(closeTable))

print(getReturnTable('2009-08-20', 7, 'CSCO'))

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
