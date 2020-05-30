import tkinter as tk
from genFunctions import plotData, plotRuns, comparePlot
from tangoFunctions import getTangoSim
from enbyFunctions import getEnbySim
from bettingFunctions import convertToML

numRuns = 18

# initalize variables
master = tk.Tk()
listTeams = [''] * 2
listPitchers = [''] * 2
listHittersA = [''] * 9
listHittersH = [''] * 9
homeT, awayT = tk.StringVar(master), tk.StringVar(master)
homeML, awayML = tk.StringVar(master), tk.StringVar(master)
homeP, awayP = tk.StringVar(master), tk.StringVar(master)
check = tk.IntVar()

# set default state of output labels
homeT.set('Away Team')
awayT.set('Home Team')


def createListTeams():
    listTeams[0] = team1Entry.get().strip().lower().replace(" ", "")
    listTeams[1] = team2Entry.get().strip().lower().replace(" ", "")
    return listTeams

def createListPitchers():
    listPitchers[0] = pitcher1Entry.get().strip().lower()
    listPitchers[1] = pitcher2Entry.get().strip().lower()
    return listPitchers

def createListHittersA():
    for i in range(9):
        listHittersA[i] = hittersA[i].get().strip().lower()

def createListHittersH():
    for i in range(9):
        listHittersH[i] = hittersH[i].get().strip().lower()

def graph():
    plotRuns(createListTeams())

def enbySim():
    if (team1Entry.get() != "") & (team2Entry.get() != "") & (pitcher1Entry.get() != "") & (pitcher2Entry.get() != ""):
        t = createListTeams()
        p = createListPitchers()

        if(not check.get()):
            y1, y2, o1, o2 = getEnbySim(t, p, 25, listHittersA, listHittersH, 0, 0)
            ml1, ml2 = convertToML(o1), convertToML(o2)
            outputSim(t, o1, o2, ml1, ml2)
            plotData(t, range(16), y1[:16], y2[:16])
        elif(check.get()):
            createListHittersA()
            createListHittersH()
            print(listHittersA)
            print(listHittersH)
            y1, y2, o1, o2 = getEnbySim(t, p, 25, listHittersA, listHittersH, 1, 1)
            ml1, ml2 = convertToML(o1), convertToML(o2)
            outputSim(t, o1, o2, ml1, ml2)
            plotData(t, range(16), y1[:16], y2[:16])

def tangoSim():
    t = createListTeams()
    p = createListPitchers()
    y1, y2, o1, o2 = getTangoSim(t, p, numRuns)
    ml1, ml2 = convertToML(o1), convertToML(o2)
    outputSim(t, o1, o2, ml1, ml2)
    plotData(t, range(numRuns), y1[:numRuns], y2[:numRuns])

def compare():
    comparePlot(numRuns)
    return

def outputSim(listTeams, home, away, ml1, ml2):
    awayT.set(listTeams[0])
    homeT.set(listTeams[1])
            
    homeP.set("{:0.2f} %".format(home))
    awayP.set("{:0.2f} %".format(away))

    if(home>away):
        homeML.set("{:0.0f}".format(ml1))
        awayML.set("+{:0.0f}".format(ml2))
    elif(home<away):
        homeML.set("+{:0.0f}".format(ml1))
        awayML.set("{:0.0f}".format(ml2))

def center_window(width, height):
    # get screen width and height
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/3) - (height/2)
    master.geometry('%dx%d+%d+%d' % (width, height, x, y))

master.title("MLB Simulator")    

# team labels and entries
tk.Label(master, text=" Away Team ", bg='dodger blue').grid(row=0, padx=6, sticky='nsew')
tk.Label(master, text=" Home Team ", bg='tomato2').grid(row=0, column=2, padx=4, sticky='nsew')
team1Entry = tk.Entry(master)
team2Entry = tk.Entry(master)
team1Entry.grid(row=0, column=1)
team2Entry.grid(row=0, column=3)

# pitcher labels and entries
tk.Label(master, text=" Starter ", bg='dodger blue').grid(row=1, column=0, padx=6, sticky='nsew')
tk.Label(master, text=" Starter ", bg='tomato2').grid(row=1, column=2, padx=4, sticky='nsew')
pitcher1Entry = tk.Entry(master, relief='groove')
pitcher2Entry = tk.Entry(master)
pitcher1Entry.grid(row=1, column=1)
pitcher2Entry.grid(row=1, column=3)    

# simulate buttons
outName0 = tk.Label(master, text="Simulate", bg='light slate gray')
outName0.grid(row=5, padx=6, sticky='nsew')
f1 = tk.Frame(master)
f1.grid(row=5, column=1, pady=5, sticky='nsew')
tk.Button(f1, text='Enby Sim', relief='groove', overrelief='sunken', command=enbySim).pack(side='left')
tk.Button(f1, text='Tango Sim', relief='groove', overrelief='sunken', command=tangoSim).pack(side='left')

# other tools buttons
outName00 = tk.Label(master, text="Other Tools", bg='light slate gray')
outName00.grid(row=6, padx=6, sticky='nsew')
f2 = tk.Frame(master)
f2.grid(row=6, column=1, sticky='nsew')
tk.Button(f2, text='    Runs    ', relief='groove', overrelief='sunken', command=graph).pack(side='left')
tk.Button(f2, text=' Compare ', relief='groove', overrelief='sunken', command=compare).pack(side='left')

# quit button
quitB = tk.Button(master, relief='groove', text='Quit', overrelief='sunken', command=master.destroy)
quitB.grid(row=16, column=5, sticky='nsew')

# results boxes
out1 = tk.Label(master, text="Win Probability", bg='yellow green')
out1.grid(row=9, column=1, pady=5, sticky='ew')
outName1 = tk.Label(master, textvariable=awayT, bg='dodger blue')
outName1.grid(row=10, padx=6, pady=0, sticky='nsew')
outName2 = tk.Label(master, textvariable=homeT, bg='tomato2')
outName2.grid(row=11, padx=6, pady=0, sticky='nsew')
entry1 = tk.Entry(master, textvariable=homeP)
entry1.grid(row=10, column=1)
entry2 = tk.Entry(master, textvariable=awayP)
entry2.grid(row=11, column=1)

outName3 = tk.Label(master, text="Moneyline", bg='yellow green')
outName3.grid(row=13, column=1, pady=5, sticky='ew')
entry3 = tk.Entry(master, textvariable=homeML)
entry3.grid(row=14, column=1)
entry4 = tk.Entry(master, textvariable=awayML)
entry4.grid(row=15, column=1)
outName4 = tk.Label(master, textvariable=awayT, bg='dodger blue')
outName4.grid(row=14, padx=6, pady=0, sticky='nsew')
outName5 = tk.Label(master, textvariable=homeT, bg='tomato2')
outName5.grid(row=15, padx=6, pady=0, sticky='nsew')

# custom lineups option
widgetList = [quitB, f1, f2, out1, outName00, outName0, outName1, outName2, outName3, outName4, outName5, entry1, entry2, entry3, entry4]
awayLU = tk.Label(text='Away Team')
homeLU = tk.Label(text='Home Team')
lineSpace = tk.Label(text='')
hitterA1 = tk.Entry()
hitterA2 = tk.Entry()
hitterA3 = tk.Entry()
hitterA4 = tk.Entry()
hitterA5 = tk.Entry()
hitterA6 = tk.Entry()
hitterA7 = tk.Entry()
hitterA8 = tk.Entry()
hitterA9 = tk.Entry()
hitterH1 = tk.Entry()
hitterH2 = tk.Entry()
hitterH3 = tk.Entry()
hitterH4 = tk.Entry()
hitterH5 = tk.Entry()
hitterH6 = tk.Entry()
hitterH7 = tk.Entry()
hitterH8 = tk.Entry()
hitterH9 = tk.Entry()

hittersA = [hitterA1, hitterA2, hitterA3, hitterA4, hitterA5, hitterA6, hitterA7, hitterA8, hitterA9]
hittersH = [hitterH1, hitterH2, hitterH3, hitterH4, hitterH5, hitterH6, hitterH7, hitterH8, hitterH9]

def addLineups():
    if(check.get()):
        for i in range(len(widgetList)):
            info = widgetList[i].grid_info()
            prev_row, prev_col, prev_padx, prev_pady, prev_sticky = int(info['row']), int(info['column']), int(info['padx']), int(info['pady']), info['sticky']
            widgetList[i].grid_forget()
            widgetList[i].grid(column=prev_col, row=prev_row+11, padx=prev_padx, pady=prev_pady, sticky=prev_sticky)

        awayLU.grid(row=3, column=1)
        homeLU.grid(row=3, column=3)
        
        hitterA1.grid(row=4, column=1)
        hitterA2.grid(row=5, column=1)
        hitterA3.grid(row=6, column=1)
        hitterA4.grid(row=7, column=1)
        hitterA5.grid(row=8, column=1)
        hitterA6.grid(row=9, column=1)
        hitterA7.grid(row=10, column=1)
        hitterA8.grid(row=11, column=1)
        hitterA9.grid(row=12, column=1)
        
        hitterH1.grid(row=4, column=3)
        hitterH2.grid(row=5, column=3)
        hitterH3.grid(row=6, column=3)
        hitterH4.grid(row=7, column=3)
        hitterH5.grid(row=8, column=3)
        hitterH6.grid(row=9, column=3)
        hitterH7.grid(row=10, column=3)
        hitterH8.grid(row=11, column=3)
        hitterH9.grid(row=12, column=3)

        lineSpace.grid(row=14, column=0)

    elif(not check.get()):
        for i in range(9):
            hittersA[i].grid_forget()
            hittersH[i].grid_forget()

        for i in range(len(widgetList)):
            info = widgetList[i].grid_info()
            prev_row, prev_col, prev_padx, prev_pady, prev_sticky = int(info['row']), int(info['column']), int(info['padx']), int(info['pady']), info['sticky']
            widgetList[i].grid_forget()
            widgetList[i].grid(column=prev_col, row=prev_row-11, padx=prev_padx, pady=prev_pady, sticky=prev_sticky)

        awayLU.grid_forget()
        homeLU.grid_forget()
        lineSpace.grid_forget()

tk.Label(master, text="Custom Lineups", relief='groove').grid(row=0, column=5, padx=5)
tk.Checkbutton(master, command=addLineups, variable=check, onvalue=1, offvalue=0).grid(row=0, column=6)

# other elements
center_window(575, 500)
tk.mainloop()
