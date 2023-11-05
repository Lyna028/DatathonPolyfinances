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

# def getTreeX(day, company):
#     treeXDict = {
#         "stockAtr" : getStockAtr(company, day, 100), # 100 est une valeur arbitraire choisi plus tard dans l'opti
#         "snpAtr" : getSnpAtr(day, 100),
#         "longReturn" : long_terme_return(company, day, 100),
#         "valueGap" : gapValue(day, 100, company),
#         "averageVolume" : averageVolume(day, 100, company),
#         "positiveReturnRatio" : getPositiveReturn(company, day, 100),
#         "marketCapRate" : getMarketCapRate(company, day, 100), ######################################
#         "marketCapAverage" : getMarketCapAverage(company, day, 100), ################################
#         "returnAverage" : getReturnAverage(company, day, 100),
#         "returnGap" : getReturnGap(company, day, 100),
#         "lowestClose" : getCloseLowHigh(company, day, 100)[0],
#         "highestClose" : getCloseLowHigh(company, day, 100)[1]
#     }
#     return treeXDict

def getTreeY(day, company, nDay):
    indexDay = closeData[closeData['timestamp'] == day].index
    return closeData.loc[indexDay[0]-nDay, 'close_' + company] - closeData.loc[indexDay[0], 'close_' + company] 

def getTreeX(day, company):
    treeXList = (getStockAtr(company, day, 100), getSnpAtr(day, 100), long_terme_return(company, day, 100), gapValue(day, 100, company),
                 averageVolume(day, 100, company), getPositiveReturn(company, day, 100), getReturnAverage(company, day, 100), 
                 getCloseLowHigh(company, day, 100)[0], getCloseLowHigh(company, day, 100)[1] )
    return treeXList

def createXbySector(sector, day):
    sectorTable = symbolInfo[symbolInfo['GICS Sector'] == sector]
    sectorSymbols = sectorTable['Symbol']
    xSectorTable = list()
    for i in sectorSymbols:
        xSectorTable.append(getTreeX(day, i))
    return xSectorTable

def createYbySector(sector, day):
    sectorTable = symbolInfo[symbolInfo['GICS Sector'] == sector]
    sectorSymbols = sectorTable['Symbol']
    ySectorTable = list()
    for i in sectorSymbols:
        ySectorTable.append(getTreeY(day, i))
    return ySectorTable


createXbySector('Industrials')