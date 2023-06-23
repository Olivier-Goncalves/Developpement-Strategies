"""
Ce fichier comporte des fonctions, des classes et des concepts pouvant être 
utile pour la programmation axé sur le trading et l'investissement
"""

import pandas as pd
import math


"""
Cette fonction détermine la déviation standard d'une liste de données. ex: les prix des close de ETHUSD
"""

def StandardDeviation(values):
    mean = pd.Series(values).mean()
    stdDeviation = 0
    stdDeviationNumerator = 0
    nValues = len(values)
    for value in values:
        if not math.isnan(value):
            stdDeviationNumerator += (value - mean)**2 
        else:
            nValues -= 1
    stdDeviation = math.sqrt(stdDeviationNumerator / nValues)

    return stdDeviation


"""
Cette fonction détermine le zscore d'une liste de données. ex: les valeurs de RSI, allant de -3 à 3 en générale
"""

def ZScore(values):
    mean = pd.Series(values).mean()
    stdDeviation = StandardDeviation(values)
    zscores = []
    for value in values:
            zscores.append((value - mean)/stdDeviation)
    return pd.Series(zscores)