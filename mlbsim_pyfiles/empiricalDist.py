import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import run data for each team
df = pd.read_excel(r'Baseball Simulator Helper.xlsx', sheet_name= '2019 Run Dist.')


def getEmpirical(boolValue):
    # get percent of games with each run total
    if(boolValue):
        runTotal = df.loc[0:19, 'runTotal'].values
        count = df.loc[0:19, 'percGames'].values

        return runTotal, count

def getPoissonEmpirical(boolValue):
    # get mean number of runs scored for all teams
    if(boolValue):

        mean = df.loc[0, 'average']

        x = 19
        allProb = [0] * x

        for i in range(x):
            probi = (mean**i * np.exp(-mean)) / np.math.factorial(i)
            allProb[i-1] = probi
    
        return allProb[0:18]
