import pandas as pd
import numpy as np
from adjustedRG import getRG


def getEnbySim(listTeams, listPitchers, numRuns, listHittersA, listHittersH, clBoolA, clBoolH):

    # get RG for both teams
    team1ARG = getRG(listTeams[0], listTeams[1], listPitchers[1], listHittersA, clBoolA)
    team2ARG = getRG(listTeams[1], listTeams[0], listPitchers[0], listHittersH, clBoolH)

    # get run distribution for both teams
    team1Prob = getEnbyGame(team1ARG, numRuns, -1) 
    team2Prob = getEnbyGame(team2ARG, numRuns, 1)

    # create matrix of probability of all combinations of scores
    probMatrix = [[0 for i in range(len(team1Prob))] for j in range(len(team2Prob))]

    for i in range(0, len(team1Prob)):
        for j in range(0, len(team2Prob)):
            probMatrix[i][j] = team1Prob[i] * team2Prob[j]

    # calculate sum probability of either team winning
    team1Wins = []
    team2Wins = []
    ties = []

    for i in range(len(probMatrix)):
        for j in range(len(probMatrix)):
            if i<j:
                team1Wins.append(probMatrix[j][i])
            elif i>j:
                team2Wins.append(probMatrix[j][i])
            elif i==j:
                ties.append(probMatrix[i][j])

    tiesProb = sum(ties) * 100
    team1WinProb = sum(team1Wins) * 100 + 0.53 * tiesProb
    team2WinProb = sum(team2Wins) * 100 + 0.47 * tiesProb
    
    extra = 100 - (team1WinProb + team2WinProb)

    ratio1 = team1WinProb / (team1WinProb + team2WinProb)
    ratio2 = team2WinProb / (team1WinProb + team2WinProb)

    team1WinProb += extra * ratio1
    team2WinProb += extra * ratio2


    return team1Prob, team2Prob, team1WinProb, team2WinProb


def getEnbyGame(adjustedRG, numRuns, hTA):
    
    if(hTA == 1):
        adjustedRG += 0.075
    elif(hTA == -1):
        adjustedRG -= 0.075
    elif(hTA == 0):
        pass
    
    RI = adjustedRG / 9

    # initialize constants and helper variables
    c = 0.767
    variance = (adjustedRG**2/9) + (adjustedRG*2/c - adjustedRG)
    r = adjustedRG**2/(variance - adjustedRG)
    B = variance/adjustedRG - 1

    a = (1 + B)**(-r)
    z = (RI/(RI + c*RI**2))**9

    # calculate shutout probabilities for negative binomial and enby
    nbProb = [0] * numRuns
    nbProb[0] = a

    enbyGameProb = [0] * numRuns
    enbyGameProb[0] = z

    # calculate unmodified nb distribution for each run total
    for k in range(1, numRuns):
        
        rS = 1

        for j in range(k):
            rS *= r + j

        nbProb[k] = rS * B**k / (np.math.factorial(k) * ((1+B)**(r+k)))
    # modify nb distribution with tango distribution
    for h in range(1, numRuns):
        enbyGameProb[h] = (1 - z) * nbProb[h] / (1 - a)

    return nbProb
    