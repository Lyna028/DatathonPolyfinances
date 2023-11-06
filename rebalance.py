import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
# from tqdm import tqdm
from sklearn.preprocessing import StandardScaler

from optimisation import optimizeWallet
actualWallet = optimizeWallet('2000-01-03')

def rebalance(day):
    optimizedWallet = optimizeWallet(day)
    actualWalletStillIn = {}
    for stock in actualWallet :
        stillInWallet = False
        for stock_ in optimizedWallet :
            if stock == stock_ :
                stillInWallet = True
        if stillInWallet:
            actualWalletStillIn[stock] = actualWallet[stock]
    actualWalletSections = {
        'Industrials' : 0,
        'Health Care' : 0,
        'Information Technology' : 0,
        'Consumer Staples' : 0,
        'Utilities' : 0,
        'Financials' : 0,
        'Materials' : 0,
        'Communication Services' : 0,
        'Consumer Discretionary' : 0,
        'Real Estate' : 0,
        'Energy' : 0
    }
    totalWeight = 0
    for key, value in actualWalletStillIn.items() :
        actualWalletSections[key[1]] += value
        totalWeight += value
    print(actualWalletSections)

    for key, value in actualWalletSections.items() : 
        if actualWalletSections[key] < 0.05 :
            for key_, value_ in optimizedWallet.items() :
                if key_[1] == key :
                    actualWalletStillIn[key_] = value_
    print(actualWalletStillIn)
    print('=============================')
    for key, value in actualWalletStillIn.items() :
        totalWeight += value
    print(actualWalletStillIn)
    print('=============================')
    if totalWeight > 1 :
        max_key = max(actualWalletStillIn, key=lambda key: actualWalletStillIn[key])
        actualWalletStillIn[max_key] -= totalWeight-1
    elif totalWeight < 1: 
        newStocks = {}
        for stock in optimizedWallet :
            notInOldWallet = True
            for stock_ in actualWalletStillIn :
                if stock == stock_ :
                    notInOldWallet = False
            if notInOldWallet : 
                newStocks[stock] = optimizedWallet[stock]
        while totalWeight < 1 and len(newStocks) != 0:
            max_key = max(newStocks, key=lambda key: newStocks[key])
            if newStocks[max_key] <= 1 - totalWeight :
                actualWalletStillIn[max_key] = newStocks[max_key]
                totalWeight += newStocks[max_key]
            else :
                actualWalletStillIn[max_key] = 1-totalWeight
                totalWeight = 1
            del newStocks[max_key]
        if totalWeight < 1 :
            max_key = max(optimizedWallet, key=lambda key: optimizedWallet[key])
            actualWalletStillIn[max_key] = 1-totalWeight

    return actualWalletStillIn
print(rebalance('2000-08-11'))
            

        
                
