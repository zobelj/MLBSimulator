import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from empiricalDist import getEmpirical, getPoissonEmpirical
from tangoFunctions import getTangoGame
from enbyFunctions import getEnbyGame


# import run data for each team
df = pd.read_excel(r'Baseball Simulator Helper.xlsx', sheet_name = '2019 Run Dist.')


def getTeamData(teamName):
    teamR = df.loc[:, teamName].values
    teamRA = df.loc[:, teamName + '1'].values

    return teamR, teamRA


def plotData(listTeams, x, y1, y2):
    # plot Poisson distribution for each team
    plt.plot(x, y1, 'bs-', label=listTeams[0])
    plt.plot(x, y2, 'rs-', label=listTeams[1])
    plt.xlabel('Number of Runs')
    plt.ylabel('Probability')
    plt.title('Runs Scored Probability')
    plt.grid(axis='both')
    plt.legend(loc='upper right')
    plt.xticks(x)
    
    plt.show()


def plotRuns(listTeams):
    # import data for specified teams
    team1R, _team1RA = getTeamData(listTeams[0])
    team2R, _team2RA = getTeamData(listTeams[1])

    # plot runs vs games for team 1
    tm1 = plt.subplot(3, 1, 1)
    tm1.plot(range(1,162), team1R[1:], 'b', label=listTeams[0])
    plt.ylabel('Runs Scored')
    plt.title('Runs Scored per Game')
    plt.legend(loc='upper right')
    plt.grid(axis='both')

    # plot runs vs games for team 2
    tm2 = plt.subplot(3, 1, 2)
    tm2.plot(range(1,162), team2R[1:], 'r', label=listTeams[1])
    plt.ylabel('Runs Scored')
    plt.legend(loc='upper right')
    plt.grid(axis='both')

    # plot run differential vs games
    tm12 = plt.subplot(3, 1, 3)
    tm12.plot(range(1,162), team1R[1:] - team2R[1:], 'g')
    plt.xlabel('Game Number')
    plt.ylabel('Run Differential')
    plt.grid(axis='both')

    plt.show()


def comparePlot(numRuns):
    # get different types of distributions
    runs, count = getEmpirical(1)
    allProb = getPoissonEmpirical(1)
    tangoGameProb = getTangoGame(df.loc[0, 'average'], numRuns, 0)
    enbyGameProb = getEnbyGame(df.loc[0, 'average'], 25, 0)

    # plot all types
    plt.bar(runs, count, color='grey', label='Empirical')
    plt.plot(range(18), allProb, 'rs-', label='Poisson')
    plt.plot(range(numRuns), tangoGameProb, 'bs-', label='Tango')
    plt.plot(range(25), enbyGameProb, 'gs-', label='Enby')
    plt.xlabel("Runs Scored")
    plt.ylabel('Frequency')
    plt.title('Poisson Distro vs Empirical Data')
    plt.xticks(range(20))
    plt.legend()

    plt.show()


def getStats(teamName):
    #import data for specified team
    team = df.loc[:, teamName].values
    
    # calculate stats
    stDev = np.std(team[1:-1])
    mean = np.mean(team[1:-1])

    return stDev, mean