import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
from combinations import findCombinations, addZeros
from adjustedRG import getRG


def getTangoDist(adjustedRG, numRuns, hTA):
    # import data for specified teams
    RI = adjustedRG / 9
    
    # add home team advantage
    if(hTA == 1):
        RI += 0.075 / 9
    elif(hTA == -1):
        RI -= 0.075 / 9        
    elif(hTA == 0):
        pass

    # initialize variables for tango calculation
    c = .767
    a = c * RI**2
    teamInn = [0] * numRuns

    # calculate probability of 0 and 1 runs
    teamInn[0] = RI / (RI + a)
    d = 1 - c * teamInn[0]
    teamInn[1] = (1 - teamInn[0]) * (1 - d)

    # calculate probability of 2+ runs
    for i in range(2, numRuns):
        teamInn[i] = teamInn[i-1] * d

    return teamInn


def nRunProb(manyLists, teamInn):

    totalProb = 0
    oneProb = 1

    for aList in manyLists:
        for i in aList:
            oneProb *= teamInn[i]
        oneProb *= len(set(permutations(aList)))
        totalProb += oneProb 
        oneProb = 1
    
    return totalProb


def getTangoGame(adjustedRG, numRuns, hTA):

    teamInn = getTangoDist(adjustedRG, numRuns, hTA)

    tangoGameProb = [0] * numRuns

    for n in range(numRuns):
        tangoGameProb[n] = nRunProb(addZeros(findCombinations(n)), teamInn) 

    return tangoGameProb


def getTangoSim(listTeams, listPitchers, numRuns):

    #team1Prob, team2Prob = parallelTeams(listTeams, numRuns, [1,-1])
    adjustedRG1 = getRG(listTeams[0], listTeams[1], listPitchers[1], [], 0)
    adjustedRG2 = getRG(listTeams[1], listTeams[0], listPitchers[0], [], 0)


    team1Prob = getTangoGame(adjustedRG1, numRuns, -1)
    team2Prob = getTangoGame(adjustedRG2, numRuns, 1)

    # create matrix of probability of all combinations of scores
    probMatrix = [[0 for i in range(len(team1Prob))] for j in range(len(team2Prob))]

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
    team1WinProb = sum(team1Wins) * 100 + 0.53 * tiesProb
    team2WinProb = sum(team2Wins) * 100 + 0.47 * tiesProb
    
    extra = 100 - (team1WinProb + team2WinProb)

    ratio1 = team1WinProb / (team1WinProb + team2WinProb)
    ratio2 = team2WinProb / (team1WinProb + team2WinProb)

    team1WinProb += extra * ratio1
    team2WinProb += extra * ratio2
    

    return team1Prob, team2Prob, team1WinProb, team2WinProb

