import pandas as pd
import numpy as np

runStats = pd.read_excel(r'Baseball Simulator Helper.xlsx', sheet_name='2019 Run Dist.')

pitcherStats = pd.read_excel(r'Baseball Simulator Helper.xlsx', sheet_name='2019 Pitcher Data')
pitcherStats['Name'] = pitcherStats['Name'].str.lower()
pitcherStats.to_dict()

hitterStats = pd.read_excel(r'Baseball Simulator Helper.xlsx', sheet_name='2019 Hitter Data')
hitterStats['Name'] = hitterStats['Name'].str.lower()
hitterStats.to_dict()

teamStats = pd.read_excel(r'Baseball Simulator Helper.xlsx', sheet_name='2019 Team Data')
teamStats['Team'] = teamStats['Team'].str.lower()
teamStats.to_dict()

teams = ['angels', 'astros', 'athletics', 'bluejays', 'braves', 'brewers', 'cardinals', 'cubs', 'diamondbacks', 'dodgers', 'giants', 'indians', 'mariners', 'marlins', 'mets', 'nationals', 'orioles', 'padres', 'phillies', 'pirates', 'rangers', 'rays', 'redsox', 'reds', 'rockies', 'royals', 'tigers', 'twins', 'whitesox', 'yankees']
hitterIndex = [0] * 9
wRC_values = [0] * 9

def getRG(teamName, oppName, oppPitcher, hitterList, clBool):
    
    # get teams R per game
    teamR = runStats.loc[:, teamName]
    teamR = np.mean(teamR[1:])
    
    #get opponents RA per game
    oppRA = runStats.loc[:, oppName + '1']
    oppRA = np.mean(oppRA[1:])

    # get pitcher ERA and IP per game
    pitcherIndex = getPitcherKey(oppPitcher)
    ERA = pitcherStats['ERA'][pitcherIndex]
    IPG = pitcherStats['IP'][pitcherIndex] / pitcherStats['GS'][pitcherIndex]

    # combine pitcher data with opponent data
    oppARA = (IPG * ERA + (9 - IPG) * oppRA) / 9

    # get wRC+ multiplier if custom lineup is entered
    if(clBool):
        for i in range(len(hitterList)):
            wRC_values[i] = hitterStats['wRC+'][getHitterKey(hitterList[i])]

        cl_wRC = np.mean(wRC_values[:])
        team_wRC = teamStats['wRC+'][teams.index(teamName)]
        wRC_ratio = cl_wRC / team_wRC
        teamR *= wRC_ratio

    # average teams scoring with opponents defense
    adjustedRG = (teamR + oppARA) / 2

    return adjustedRG


def calcRunsFor(teamName):
    
    # get teams R per game
    teamR = runStats.loc[:, teamName]
    teamR = np.mean(teamR[1:])

    # get teams wRC+ 


def getPitcherKey(val):
    for key, value in pitcherStats['Name'].items():
        if val == value:
            return key

def getHitterKey(val):
    for key, value in hitterStats['Name'].items():
        if val == value:
            return key

