import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

def getTR(high, low, close) :
    return max( high-low, high-close, low-close)

def createAtr(lastsHigh, lastsLow, lastsClose, nValue) :
    sum = 0
    for high, low, close in zip(lastsHigh, lastsLow, lastsClose) :
        sum += getTR(high, low, close)
    return sum/nValue


def updateAtr(lastAtr, high, low, close) :
    return (lastAtr + getTR(high, low, close))