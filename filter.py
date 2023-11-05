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
symbolInfo = pd.read_csv(os.path.join(path, 'series/additional_data/SP500_symbol_info.csv'))

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
    return normaliseAjustedCloseData.loc[indexDay[0], 'adjusted_close_' + stock] - normaliseAjustedCloseData.loc[indexDay[0]+durationDays, 'adjusted_close_' + stock]

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
    return (selectionnedDataCompany.min(), selectionnedDataCompany.max())


# print(getCloseLowHigh('2014-12-31', 4, 'CSCO'))
def getReturnAverage(stock, dayOne, nDay):
    myList = getReturnTable(dayOne, nDay, stock)
    sumReturn = 0
    for i in myList:
        sumReturn += i
    return sumReturn/nDay
# print(getReturnAverage( 'CSCO', '2003-12-31', 4))

def getReturnGap(stock, dayOne, nDay):
    myList = getReturnTable(dayOne, nDay, stock)
    return max(myList) - min(myList)

def getPositiveReturn(stock, currentDay, durationDays):
    nPositiveDays = 0
    table = getReturnTable(currentDay, durationDays, stock)
    for i in table:
        nPositiveDays += 1 if i > 0 else 0
    return nPositiveDays/durationDays*100

def getTR(high, low, close) :
    return max( high-low, high-close, low-close)

def createAtr(lastsHigh, lastsLow, lastsClose, nValue) :
    sum = 0
    for high, low, close in zip(lastsHigh, lastsLow, lastsClose) :
        sum += getTR(high, low, close)
    return sum/nValue

def getStockAtr(company, day, nDay):
    highIndex = highData[highData['timestamp'] == day ].index
    highTable = highData.iloc[highIndex[0] : highIndex[0] + nDay + 1]

    lowIndex = lowData[lowData['timestamp'] == day ].index
    lowTable = lowData.iloc[lowIndex[0] : lowIndex[0] + nDay + 1]

    closeIndex = closeData[closeData['timestamp'] == day ].index
    closeTable = closeData.iloc[closeIndex[0] : closeIndex[0] + nDay + 1]

    return createAtr(highTable['high_' + company], lowTable['low_' + company], closeTable['close_' + company], nDay) 


def getSnpAtr(day, nDay):
    highIndex = highData[highData['timestamp'] == day ].index
    highTable = highData.iloc[highIndex[0] : highIndex[0] + nDay + 1]

    lowIndex = lowData[lowData['timestamp'] == day ].index
    lowTable = lowData.iloc[lowIndex[0] : lowIndex[0] + nDay + 1]

    closeIndex = closeData[closeData['timestamp'] == day ].index
    closeTable = closeData.iloc[closeIndex[0] : closeIndex[0] + nDay + 1]

    return createAtr(highTable['high'], lowTable['low'], closeTable['close_'], nDay)  # A TESTER


def getTreeY(day, company, nDay):
    indexDay = ajustedCloseData[ajustedCloseData['timestamp'] == day].index
    rendementVal = ajustedCloseData.loc[indexDay[0]-nDay, 'adjusted_close_' + company] - ajustedCloseData.loc[indexDay[0], 'adjusted_close_' + company]

    return rendementVal/closeData.loc[indexDay[0], 'close_' + company] * 100

def getTreeX(day, company):
    treeXList = (getStockAtr(company, day, 100), long_terme_return(day, 100, company), gapValue(day, 100, company),
                 averageVolume(day, 100, company), getPositiveReturn(company, day, 100), getReturnAverage(company, day, 100), 
                 getCloseLowHigh(day, 100, company)[0], getCloseLowHigh(day, 100, company)[1] )
    return treeXList

def createXbySector(sector, day):
    sectorTable = symbolInfo[symbolInfo['GICS Sector'] == sector]
    sectorSymbols = sectorTable['Symbol']
    xSectorTable = list()
    indexDate = openData[openData['timestamp'] == day].index
    for i in sectorSymbols:
        for j in range(25):
            actualDay = openData.loc[indexDate[0] + j*5, 'timestamp']
            xSectorTable.append(getTreeX(actualDay, i))
    return xSectorTable



def createYbySector(sector, day):
    sectorTable = symbolInfo[symbolInfo['GICS Sector'] == sector]
    sectorSymbols = sectorTable['Symbol']
    ySectorTable = list()
    indexDate = openData[openData['timestamp'] == day].index
    for i in sectorSymbols:
        for j in range(25):
            actualDay = openData.loc[indexDate[0] + j*5, 'timestamp']
            ySectorTable.append(getTreeY(actualDay, i, 100))
    return ySectorTable

# print(createYbySector('Industrials', '2013-11-05'))
# print(createYbySector('Industrials', '2013-11-05'))

# createXbySector('Industrials')