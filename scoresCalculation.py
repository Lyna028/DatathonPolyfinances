import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib


def averageVolume(currentDay, durationDays, company) :
    return 1

def gapValue ( startDate, duration,company):
    return 0 ###################################################################################################### bug a regler

def getPositiveReturn(stock, currentDay, durationDays):

    return 1

def getATR(lastsHigh, lastsLow, lastsClose, nValue):
    return 1 ###################################################################################################### A VÉRIFIER

def getMarketCapRate(actionName, startingDay, duration) :
    indexFirstDay = marketCapDefaultData[marketCapDefaultData['date'] == startingDay].index
    indexLastDay = marketCapDefaultData[marketCapDefaultData['date'] == startingDay + duration].index

    valueFirstDay = marketCapDefaultData.loc[indexFirstDay[0], actionName]
    valueLastDay = marketCapDefaultData.loc[indexLastDay[0], actionName]

    return valueLastDay/valueFirstDay * 100 ####################################################################### Toujour à vérifier

def getMarketCapAverage(stock, dayOne, nDay): 
    return 0 ###################################################################################################### PAS FAIT

def getReturnAverage(stock, dayOne, nDay):
    table = getReturnTable(dayOne, nDay, stock)
    sumReturn = 0
    for i in table:
        sum += i
    return sum/nDay

def getReturnGap(stock, dayOne, nDay):
    myList = getReturnTable(dayOne, nDay, stock)
    return max(myList) - min(myList)

def getStockAtr(company, day, nDay):
    highIndex = highData[highData['timestamp'] == day ].index
    highTable = highData.iloc[closeIndex[0] : closeIndex[0] + nDay + 1]

    lowIndex = lowData[lowData['timestamp'] == day ].index
    lowTable = lowData.iloc[closeIndex[0] : closeIndex[0] + nDay + 1]

    closeIndex = closeData[closeData['timestamp'] == day ].index
    closeTable = closeData.iloc[closeIndex[0] : closeIndex[0] + nDay + 1]

    return getATR(highTable['high_' + company], lowTable['low_' + company], closeTable['close_' + company], nDay) #### A TESTER

def getSnpAtr(day, nDay):
    highIndex = highData[highData['timestamp'] == day ].index
    highTable = highData.iloc[closeIndex[0] : closeIndex[0] + nDay + 1]

    lowIndex = lowData[lowData['timestamp'] == day ].index
    lowTable = lowData.iloc[closeIndex[0] : closeIndex[0] + nDay + 1]

    closeIndex = closeData[closeData['timestamp'] == day ].index
    closeTable = closeData.iloc[closeIndex[0] : closeIndex[0] + nDay + 1]

    return getATR(highTable['high'], lowTable['low'], closeTable['close_'], nDay)  ################################## A TESTER
 

def long_terme_return( stock, currentDay, durationDays):
    indexDay = normaliseAjustedCloseData[normaliseAjustedCloseData['timestamp'] == currentDay].index
    print(normaliseAjustedCloseData.loc[indexDay[0], stock])
    print(normaliseAjustedCloseData.loc[indexDay[0]+durationDays, stock])
    return normaliseAjustedCloseData.loc[indexDay[0], stock] - normaliseAjustedCloseData.loc[indexDay[0]+durationDays, stock]


def getCloseLowHigh(company, dayOne, nDay):
    closeTable = list()

    closeIndex = closeData[closeData['timestamp'] == dayOne ].index
    closeTable = closeData.iloc[closeIndex[0] : closeIndex[0] + nDay + 1]

    for i in closeTable['close_' + company]:
        closeTable.append(i)
    return (min(closeTable), max(closeTable))

def getTreeX(day, company):
    treeXDict = {
        "stockAtr" : getStockAtr(company, day, 100), # 100 est une valeur arbitraire choisi plus tard dans l'opti
        "snpAtr" : getSnpAtr(day, 100),
        "longReturn" : long_terme_return(company, day, 100),
        "valueGap" : gapValue(day, 100, company),
        "averageVolume" : averageVolume(day, 100, company),
        "positiveReturnRatio" : getPositiveReturn(company, day, 100),
        "marketCapRate" : getMarketCapRate(company, day, 100),
        "marketCapAverage" : getMarketCapAverage(company, day, 100),
        "returnAverage" : getReturnAverage(company, day, 100),
        "returnGap" : getReturnGap(company, day, 100),
        "lowestClose" : getCloseLowHigh(company, day, 100)[0],
        "highestClose" : getCloseLowHigh(company, day, 100)[1]
    }
    return treeXDict

def getTreeY(day, company, nDay):
    indexDay = normaliseAjustedCloseData[normaliseAjustedCloseData['timestamp'] == day].index
    return normaliseAjustedCloseData.loc[indexDay[0]-nDay, company] - normaliseAjustedCloseData.loc[indexDay[0], company] 