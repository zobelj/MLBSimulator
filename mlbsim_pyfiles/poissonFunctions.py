import pandas as pd
import numpy as np
from genFunctions import getTeamData, plotData


df = pd.read_excel(r'Baseball Simulator Helper.xlsx', sheet_name = '2019 Run Dist.')

def getPoissonDist(teamName, numRuns, hTA):
    # import data for specified teams 
    teamR, _teamRA = getTeamData(teamName)

    hTA = 0.075 # home team advantage (runs)
    mean = np.mean(teamR[1:-1])

    if(hTA == 1):
        mean += hTA
    elif(hTA == -1):
        mean -= hTA
    elif(hTA == 0):
        pass

    teamProb = [0] * numRuns

    # calculate probability of scoring a given number of runs
    for i in range(numRuns):
        probi = (mean**i * np.exp(-mean)) / np.math.factorial(i)

        teamProb[i-1] = probi

    return teamProb[0:len(teamProb)-1]
    

def getPoissonSim(listTeams, numRuns):
    team1Prob, team2Prob = getPoissonDist(listTeams[0], numRuns, 1), getPoissonDist(listTeams[1], numRuns, 0)

    # create matrix of probability of all combinations of scores
    probMatrix = [[0 for i in range(numRuns)] for j in range(numRuns)]

    for i in range(0, len(team1Prob)):
        for j in range(0, len(team2Prob)):
            probMatrix[i][j] = team1Prob[i] * team2Prob[j]

    # calculate sum probability of either team winning
    team1Wins = []
    team2Wins = []
    ties = []

    for i in range(0, len(probMatrix)):
        for j in range(0, len(probMatrix)):
            if i<j:
                team1Wins.append(probMatrix[j][i])
            elif i>j:
                team2Wins.append(probMatrix[j][i])
            elif i==j:
                ties.append(probMatrix[i][j])

    tiesProb = sum(ties) * 100
    team1WinProb = sum(team1Wins) * 100 + 0.5 * tiesProb
    team2WinProb = sum(team2Wins) * 100 + 0.5 * tiesProb
    total = team1WinProb + team2WinProb
    
    # print probabilities to console
    print("\n{}: {:0.2f} %".format(listTeams[0], team1WinProb))
    print("{}: {:0.2f} %".format(listTeams[1], team2WinProb))
    print("Total: {:0.2f} %\n".format(total))
