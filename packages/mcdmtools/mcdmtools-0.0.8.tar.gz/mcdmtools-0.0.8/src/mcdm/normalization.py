import pandas as pd
import numpy 

def vektorizeNormalization(dm, profitcost):
    """kriterlerin fayda ya da maliyet odaklı olması durumuna göre\
        normalizasyon gerçekleştirilir"""
    squared = lambda x: x*x
    dm_norm = pd.DataFrame()
    for i in profitcost.columns:
        if profitcost.loc[0,i] == 'max':
            dm_norm[i] = dm[i] / squared(dm[i]).sum(axis=0)**0.5
        elif profitcost.loc[0,i]=='min':
             dm_norm[i] = 1- (dm[i] / squared(dm[i]).sum(axis=0)**0.5)
    return dm_norm