import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

def getReturnByDay(entry, close):
    return (entry-close)/entry * 100

