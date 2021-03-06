# imports classes needed for tkinter -- the gui library
from __future__ import division
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import csv

# imports classes needed for the graph creation
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from pylab import *
import time
import pandas as pd


#####################
filenameClass = ""  # path of the class file
xcldata = list()  # stores the class data in a list
nrc = 0  # number of rows class file
ncc = 0  # number of columns class file
xclass = set()  # stores the class data in a set
ctxclass = list()  # stores the class data in a list
allclass = set() # store the class and non-class data in a set
######################
filenameNominal = ""
ncldata = list()  # stores the non-class data in a list
nrn = 0   # number of rows nominal file
ncn = 0  # number of columns nominal file
nonclass = set()  # store the non-class data in a set
######################
# variables for storing the total number of combinations at 2,3, and 4-way testing
nvals = []
ncoms2 = 0
ncoms3 = 0
ncoms4 = 0
# variables for storing the total values at 2,3, and 4-way testing
totvals1 = 0
totvals2 = 0
totvals3 = 0
totvals4 = 0
######################
# Variables to check the class and nominal files have loaded
stateClassFile = False
stateNominalFile = False
stateOutputFile = False

# output variables
filenameOutput = ""
coverageLevel = 2


# action for the button object BtnLoadFaultFile
# prompts the user to pick the class file and
# then loads its contents into arrays
def BtnLoadFaultFile_Click():
    # prompts the user to select a file
    global filenameClass
    filenameClass = filedialog.askopenfilename(initialdir="/", title="Select Class File")

    # puts file name in the GUI
    txtFaultContents.insert(0, filenameClass)

    # checks that a destination was selected
    if filenameClass != '':
        global stateClassFile
        stateClassFile = True
        # load nominal, non-class file into array
        global xcldata
        with open(filenameClass) as csvfile:
            xcldata = list(csv.reader(csvfile))

        # put the data in the faultList to show on screen
        for entry in xcldata:
            faultList.insert(END, ' '.join(entry))
        faultList.grid(row=2, column=1)
        txtFaultInfo.config(command=faultList.yview)

        loadClassFile()


# loads the class file and it contents into the GUI
def loadClassFile():
    global nrc
    nrc = len(xcldata)  # N rows class, row count
    global ncc
    ncc = len(xcldata[0])  # N cols class, col count
    global xclass
    xclass = [set() for _ in range(ncc)]
    global ctxclass
    ctxclass = [list() for _ in range(ncc)]  # store all values for counting later
    global allclass
    allclass = [set() for _ in range(ncc)]  # store both class and non-class data

    # populates the arrays with the class data
    for j in range(ncc):
        for i in range(nrc):
            xclass[j].add(xcldata[i][j])
            ctxclass[j].append(xcldata[i][j])
            allclass[j].add(xcldata[i][j])


# actions when load nominal file btn is clicked
# prompts the user to pick a non-class/nominal file
def nomButton_Click():
    # prompts user to pick a file from their computer
    global filenameNominal
    filenameNominal = filedialog.askopenfilename(initialdir="/", title="Select Nominal File")
    txtNominalInfo.insert(0, filenameNominal)
    global stateNominalFile
    stateNominalFile = True

    # checks if the user selected a file
    if filenameNominal != '':
        # checks that there is a class and non-class file loaded
        if stateNominalFile == True and stateClassFile == True:
            btnTest['state'] = ACTIVE

        # loads the non-class data
        global ncldata
        with open(filenameNominal) as csvfile:
            ncldata = list(csv.reader(csvfile))

        loadNomFile()


# loads the nominal fault file into the program
def loadNomFile():
    # determines certain attributes about the shape of the nominal data
    global nrn
    nrn = len(ncldata)
    global ncn
    ncn = len(ncldata[0])
    if ncn != ncc:
        raise IOError("Both files must have same number of parameters")

    global nonclass
    nonclass = [set() for _ in range(ncn)]

    # populates the arrays with non-class data
    for j in range(ncn):
        for i in range(nrn):
            nonclass[j].add(ncldata[i][j])
            allclass[j].add(ncldata[i][j])


# action for when the run button is clicked
# determines which combination levels are to be run
# based on the users selections
def btnTest_Click():
    computeValueSettings()
    # checks which levels of coverage the user selected
    if var1Way.get() == 1:
        get1WayResults()
    if var2Way.get() == 1:
        get2WayResults()
        #produce2WayDifferenceStats()
    if var3Way.get() == 1:
        getThreeWayResults()
        #produceThreeWayDifferenceStats()
    if var4Way.get() == 1:
        getFourWayResults()
        #produceFourWayDifferenceStats()
    if var5Way.get() == 1:
        getFiveWayResults()
    if var6Way.get() == 1:
        getSixWayResults()


# Computes the statistics needed for the finding making the difference plots
def computeValueSettings():
    global nvals
    nvals = []
    for i in range(ncc):
        vset = (xclass[i].copy()).union(nonclass[i])
        nvals.append(len(vset))

    # finds the number of combinations in 2,3 and 4 way data
    global ncoms2
    global ncoms3
    global ncoms4
    ncoms2 = int(math.factorial(ncc) / (2 * math.factorial(ncc - 2)))
    ncoms3 = int(math.factorial(ncc) / (6 * math.factorial(ncc - 3)))
    ncoms4 = int(math.factorial(ncc) / (24 * math.factorial(ncc - 4)))

    # finds the number of values in 1,2,3,4 way testing
    global totvals1
    global totvals2
    global totvals3
    global totvals4
    totvals1 = sum(nvals[i] for i in range(ncc))
    totvals2 = sum(nvals[i] * nvals[j] for i in range(ncc - 1) for j in range(i + 1, ncc))
    totvals3 = sum(nvals[i] * nvals[j] * nvals[k] for i in range(ncc - 2) for j in range(i + 1, ncc - 1) for k in
                   range(j + 1, ncc))
    totvals4 = sum(nvals[i] * nvals[j] * nvals[k] * nvals[m] for i in range(ncc - 3) for j in range(i + 1, ncc - 2)
                   for k in range(j + 1, ncc - 1) for m in range(k + 1, ncc))


# creates the difference plots for two-way combinations
def produce2WayDifferenceStats():
    # set up 2way difference sets
    start2way = datetime.datetime.now()
    diff2way = [list() for _ in range(ncc - 1)]
    diff2cnts = []
    for i in range(ncc - 1):
        diff2way[i] = [set() for _ in range(ncc)]

    # load 2way combinations for xclass data,
    xclass2w = [list() for _ in range(ncc - 1)]
    ctxclass2w = [list() for _ in range(ncc - 1)]
    allclass2w = [list() for _ in range(ncc - 1)]

    for i in range(ncc - 1):
        xclass2w[i] = [set() for _ in range(ncc)]
        ctxclass2w[i] = [list() for _ in range(ncc)]
        allclass2w[i] = [set() for _ in range(ncc)]

    for r in range(nrc):
        for i in range(ncc - 1):
            for j in range(i + 1, ncc):
                xclass2w[i][j].add((xcldata[r][i], xcldata[r][j]))
                ctxclass2w[i][j].append((xcldata[r][i], xcldata[r][j]))
                allclass2w[i][j].add((xcldata[r][i], xcldata[r][j]))

    # load 2way combinations for nonclass data
    nclass2w = [list() for _ in range(ncc - 1)]
    for i in range(ncc - 1):
        nclass2w[i] = [set() for _ in range(ncc)]

    for r in range(nrn):
        for i in range(ncc - 1):
            for j in range(i + 1, ncc):
                # print("add",r,i,j)
                nclass2w[i][j].add((ncldata[r][i], ncldata[r][j]))
                allclass2w[i][j].add((ncldata[r][i], ncldata[r][j]))

    # get 2way set diff class \ nonclass
    for i in range(ncc - 1):
        for j in range(i + 1, ncc):
            diff2way[i][j] = xclass2w[i][j].difference(nclass2w[i][j])
    sys.stderr.write("2way diffs done {0}\n".format(datetime.datetime.now()))

    for i in range(ncc):
        for rf in range(1, nrc):
            in_pass_count = 0
            for rp in range(nrn):
                if (xcldata[rf][i] == ncldata[rp][i]):
                    in_pass_count += 1

            output = "{0} occurrences = {1} of cases, {2} = {3}\n".format(in_pass_count, in_pass_count / (nrn - 1),
                                                                          xcldata[0][i],
                                                                          xcldata[rf][i])

    # creates and outputs two way coverage plots
    yvals2 = []
    for i in range(ncc - 1):
        for j in range(i + 1, ncc):
            yvals2.append(len(xclass2w[i][j]) / (nvals[i] * nvals[j]))
    xvals2 = range(ncoms2)
    # Coverage as in CCM;  completeness

    plt.figure(figsize=(12, 5))

    subplot(121)
    plt.title("class com coverage")
    plt.ylim(0, 1)
    plt.xlim(0, 1)
    yvals2.sort()
    # sfy2 = max(yvals2)  #scale factor for y
    sfx2 = ncoms2
    yvals2.reverse()

    X2 = array(xvals2)
    Y2 = array(yvals2)
    Xd2 = X2 / sfx2
    plot = plt.figure(figsize=(3, 3))
    plt.figaspect(.5)
    plt.plot(Xd2, Y2, color="red", label="2-way")

    # create a canvas and display it on the screen
    canvas2Way = FigureCanvasTkAgg(plot, twoWayTab)
    canvas_widget = canvas2Way.get_tk_widget()
    canvas_widget.grid(row=3, column=0)


# collects the occurrences of one-way combination of class parameters in the
# non-class(nclData) files
def get1WayResults():
    start_time = time.time()  # starts a timer to time to two-way combinations
    output = ""
    file = open("1Wayresults.csv", "a")  # opens the output file
    file.write("occurrences,pct,param,value,nrn\n")
    # determines for each combination the number of occurrences in the non-class file
    for i in range(ncc):
        for rf in range(1, nrc):
            in_pass_count = 0
            for rp in range(1, nrn):
                if xcldata[rf][i] == ncldata[rp][i]:
                    in_pass_count += 1
            output = "{0},{1},{2},{3},{4}\n".format(in_pass_count, in_pass_count / (nrn - 1), xcldata[0][i], xcldata[rf][i], nrn-1)
            file.write(output)  # writes the result of the current combination to the output file

    file.close()
    print("1-Way runtime %s" % (time.time() - start_time))  # outputs the time the occurrence gathering took


# collects the occurrences of two-way combination of class parameters in the
# non-class(nclData) files
def get2WayResults():
    start_time = time.time()  # starts a timer to time to two-way combinations
    output = ""
    file = open("2Wayresults.csv", "a")  # opens the output file
    file.write("occurrences,pct,param1,param2,value1,value2,nrn\n")
    # determines for each combination the number of occurrences in the non-class file
    for i in range(ncc - 1):
        for j in range(i + 1, ncc):
            for rf in range(1, nrc):
                in_pass_count = 0
                for rp in range(1, nrn):
                    if xcldata[rf][i] == ncldata[rp][i] and xcldata[rf][j] == ncldata[rp][j]:
                        in_pass_count += 1
                output = "{0},{1},{2},{3},{4},{5},{6}\n".format(in_pass_count, in_pass_count / (nrn - 1), xcldata[0][i], xcldata[0][j], xcldata[rf][i], xcldata[rf][j],nrn-1)
                file.write(output)  # writes the result of the current combination to the output file

    file.close()
    print("2-Way runtime %s" % (time.time() - start_time))  # outputs the time the occurrence gathering took


# creates the difference plots for three-way combinations
def produceThreeWayDifferenceStats():
    # set up 3way difference sets
    start3way = datetime.datetime.now()
    diff3way = [[list() for _ in range(ncc)] for _ in range(ncc)]
    diff3cnts = []
    for i in range(ncc - 2):
        for j in range(i + 1, ncc - 1):
            diff3way[i][j] = [set() for _ in range(ncc)]

    # load 3-way combinations for xclass data
    xclass3w = [[list() for _ in range(ncc)] for _ in range(ncc)]
    ctxclass3w = [[list() for _ in range(ncc)] for _ in range(ncc)]
    allclass3w = [[list() for _ in range(ncc)] for _ in range(ncc)]

    for i in range(ncc - 2):
        for j in range(i + 1, ncc - 1):
            xclass3w[i][j] = [set() for _ in range(ncc)]
            ctxclass3w[i][j] = [list() for _ in range(ncc)]
            allclass3w[i][j] = [set() for _ in range(ncc)]

    for r in range(nrc):
        for i in range(ncc - 2):
            for j in range(i + 1, ncc - 1):
                for k in range(j + 1, ncc):
                    # print("add",r,i,j)
                    xclass3w[i][j][k].add((xcldata[r][i], xcldata[r][j], xcldata[r][k]))
                    ctxclass3w[i][j][k].append((xcldata[r][i], xcldata[r][j], xcldata[r][k]))
                    allclass3w[i][j][k].add((xcldata[r][i], xcldata[r][j], xcldata[r][k]))

    # load 3-way combinations for nclass data
    nclass3w = [[list() for _ in range(ncc)] for _ in range(ncc)]
    for i in range(ncc - 2):
        for j in range(i + 1, ncc - 1):
            nclass3w[i][j] = [set() for _ in range(ncc)]

    for r in range(nrn):
        for i in range(ncc - 2):
            for j in range(i + 1, ncc - 1):
                for k in range(j + 1, ncc):
                    # print("add",r,i,j)
                    nclass3w[i][j][k].add((ncldata[r][i], ncldata[r][j], ncldata[r][k]))
                    allclass3w[i][j][k].add((ncldata[r][i], ncldata[r][j], ncldata[r][k]))

    # get 3way set diff class \ nonclass
    for i in range(ncc - 2):
        for j in range(i + 1, ncc - 1):
            for k in range(j + 1, ncc):
                diff3way[i][j][k] = xclass3w[i][j][k].difference(nclass3w[i][j][k])
    sys.stderr.write("3way diffs done {0}\n".format(datetime.datetime.now()))

    # display graph for diffs
    yvals3 = []
    for i in range(ncc - 2):
        for j in range(i + 1, ncc - 1):
            for k in range(j + 1, ncc):
                yvals3.append(len(xclass3w[i][j][k]) / (nvals[i] * nvals[j] * nvals[k]))
    xvals3 = range(ncoms3)
    yvals3.sort()
    sfx3 = ncoms3
    yvals3.reverse()

    X3 = array(xvals3)
    Y3 = array(yvals3)
    Xd3 = X3 / sfx3
    plot = plt.figure(figsize=(3, 3))
    plt.plot(Xd3, Y3, color="blue", label="3-way")

    # create a canvas and display it on the screen
    canvas3Way = FigureCanvasTkAgg(plot, threeWayTab)
    canvas_widget = canvas3Way.get_tk_widget()
    canvas_widget.grid(row=3, column=0)


# collects the occurrences of three-way combination of class parameters in the
# and non-class(nclData) file
def getThreeWayResults():
    # output 3way diffs
    start_time = time.time()  # starts a timer to time to three-way combinations
    file = open("3Wayresults.csv", "a")
    file.write("occurrences,pct,param1,param2,param3,value1,value2,value3,nrn\n")

    # determines for each combination the number of occurrences in the non-class file
    for i in range(ncc - 2):
        for j in range(i + 1, ncc - 1):
            for k in range(j + 1, ncc):
                for rf in range(1, nrc):
                    in_pass_count = 0
                    for rp in range(1, nrn):
                        if (xcldata[rf][i] == ncldata[rp][i] and xcldata[rf][j] == ncldata[rp][j] and xcldata[rf][k] ==
                                ncldata[rp][k]):
                            in_pass_count += 1
                    output = "{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(in_pass_count,
                                                                                         in_pass_count / (nrn - 1),
                                                                                         xcldata[0][i], xcldata[0][j],
                                                                                         xcldata[0][k], xcldata[rf][i],
                                                                                         xcldata[rf][j], xcldata[rf][k],nrn-1)
                    file.write(output)  # writes the result of the current combination to the output file

    file.close()
    print("3-Way runtime %s" % (time.time() - start_time))  # outputs the time the occurrence gathering took


# generates the difference stats and outputs that to the GUI in the form of a graph
# for 4-wy combinations
def produceFourWayDifferenceStats():
    # set up 4way difference sets
    diff4way = [[[list() for _ in range(ncc)] for _ in range(ncc)] for _ in range(ncc)]
    diff4cnts = []
    for i in range(ncc - 3):
        for j in range(i + 1, ncc - 2):
            for k in range(j + 1, ncc - 1):
                diff4way[i][j][k] = [set() for _ in range(ncc)]

    # load 4-way combinations for xclass data
    xclass4w = [[[list() for _ in range(ncc)] for _ in range(ncc)] for _ in range(ncc)]
    ctxclass4w = [[[list() for _ in range(ncc)] for _ in range(ncc)] for _ in range(ncc)]
    allclass4w = [[[list() for _ in range(ncc)] for _ in range(ncc)] for _ in range(ncc)]

    for i in range(ncc - 3):
        for j in range(i + 1, ncc - 2):
            for k in range(j + 1, ncc - 1):
                xclass4w[i][j][k] = [set() for _ in range(ncc)]
                ctxclass4w[i][j][k] = [list() for _ in range(ncc)]
                allclass4w[i][j][k] = [set() for _ in range(ncc)]

    for r in range(nrc):
        for i in range(ncc - 3):
            for j in range(i + 1, ncc - 2):
                for k in range(j + 1, ncc - 1):
                    for m in range(k + 1, ncc):
                        xclass4w[i][j][k][m].add((xcldata[r][i], xcldata[r][j], xcldata[r][k], xcldata[r][m]))
                        ctxclass4w[i][j][k][m].append((xcldata[r][i], xcldata[r][j], xcldata[r][k], xcldata[r][m]))
                        allclass4w[i][j][k][m].add((xcldata[r][i], xcldata[r][j], xcldata[r][k], xcldata[r][m]))

    # load 4-way combinations for nonclass data
    nclass4w = [[[list() for _ in range(ncc)] for _ in range(ncc)] for _ in range(ncc)]
    for i in range(ncc - 3):
        for j in range(i + 1, ncc - 2):
            for k in range(j + 1, ncc - 1):
                nclass4w[i][j][k] = [set() for _ in range(ncc)]

    for r in range(nrn):
        for i in range(ncc - 3):
            for j in range(i + 1, ncc - 2):
                for k in range(j + 1, ncc - 1):
                    for m in range(k + 1, ncc):
                        nclass4w[i][j][k][m].add((ncldata[r][i], ncldata[r][j], ncldata[r][k], ncldata[r][m]))
                        allclass4w[i][j][k][m].add((ncldata[r][i], ncldata[r][j], ncldata[r][k], ncldata[r][m]))

    # get 4way set diff class \\ nonclass
    for i in range(ncc - 3):
        for j in range(i + 1, ncc - 2):
            for k in range(j + 1, ncc - 1):
                for m in range(k + 1, ncc):
                    diff4way[i][j][k][m] = xclass4w[i][j][k][m].difference(nclass4w[i][j][k][m])
    sys.stderr.write("4way diffs done {0}\n".format(datetime.datetime.now()))

    # 4way coverage plot
    yvals4 = []
    for i in range(ncc - 3):
        for j in range(i + 1, ncc - 2):
            for k in range(j + 1, ncc - 1):
                for m in range(k + 1, ncc):
                    yvals4.append(len(xclass4w[i][j][k][m]) / (nvals[i] * nvals[j] * nvals[k] * nvals[m]))
    xvals4 = range(ncoms4)
    yvals4.sort()
    sfx4 = ncoms4
    yvals4.reverse()

    X4 = array(xvals4)
    Y4 = array(yvals4)
    Xd4 = X4 / sfx4
    plot = plt.figure(figsize=(3, 3))
    plt.plot(Xd4, Y4, color="blue", label="4-way")

    # create a canvas and display it on the screen
    canvas4Way = FigureCanvasTkAgg(plot, fourWayTab)
    canvas_widget = canvas4Way.get_tk_widget()
    canvas_widget.grid(row=3, column=0)


# collects the occurrences of four-way combination of class parameters in the
# non-class(nclData) file
def getFourWayResults():
    start_time = time.time()  # starts a timer to time to four-way combinations
    output = ""
    file = open("4Wayresults.csv", "a")
    file.write("occurrences,pct,param1,param2,param3,param4,value1,value2,value3,value4,nrn\n")
    # determines for each combination the number of occurrences in the non-class file
    for i in range(ncn-3):
        for j in range(i+1, ncn-2):
            for k in range(j+1, ncn-1):
                for l in range(k+1, ncn):
                    for rf in range(1, nrc):
                        in_pass_count = 0
                        for rp in range(1, nrn):
                            if (xcldata[rf][i] == ncldata[rp][i] and xcldata[rf][j] == ncldata[rp][j] and xcldata[rf][k] == ncldata[rp][k] and xcldata[rf][l] == ncldata[rp][l]):
                                in_pass_count += 1
                        output = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n".format(in_pass_count,
                                                                                             in_pass_count / (nrn - 1),
                                                                                             xcldata[0][i],
                                                                                             xcldata[0][j],
                                                                                             xcldata[0][k],
                                                                                             xcldata[0][l],
                                                                                             xcldata[rf][i],
                                                                                             xcldata[rf][j],
                                                                                             xcldata[rf][k],
                                                                                             xcldata[rf][l],nrn-1)
                        file.write(output)  # writes the result of the current combination to the output file

    file.close()
    print("4-Way runtime %s" % (time.time() - start_time))  # outputs the time the occurrence gathering took


# collects the occurrences of five-way combination of class parameters in the
# non-class(nclData) files
def getFiveWayResults():
    start_time = time.time()  # starts a timer to time to four-way combinations
    output = ""
    file = open("5Wayresults.csv", "a")
    file.write("occurrences,pct,param1,param2,param3,param4,param5,value1,value2,value3,value4,value5,nrn\n")

    # determines for each combination the number of occurrences in the non-class file
    for i in range(ncn - 4):
        for j in range(i + 1, ncn - 3):
            for k in range(j + 1, ncn - 2):
                for l in range(k + 1, ncn - 1):
                    for m in range(l + 1, ncn):
                        for rf in range(1, nrc):
                            in_pass_count = 0
                            for rp in range(1, nrn):
                                if (xcldata[rf][i] == ncldata[rp][i] and xcldata[rf][j] == ncldata[rp][j] and xcldata[rf][k] == ncldata[rp][k] and xcldata[rf][l] == ncldata[rp][l] and xcldata[rf][m] == ncldata[rp][m]):
                                    in_pass_count += 1
                            output = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}\n".format(
                                in_pass_count,
                                in_pass_count / (nrn - 1),
                                xcldata[0][i],
                                xcldata[0][j],
                                xcldata[0][k],
                                xcldata[0][l],
                                xcldata[0][m],
                                xcldata[rf][i],
                                xcldata[rf][j],
                                xcldata[rf][k],
                                xcldata[rf][l],
                                xcldata[rf][m],nrn-1)
                            file.write(output) # writes the result of the current combination to the output file

    file.close()
    print("5-Way runtime %s" % (time.time() - start_time))  # outputs the time the occurrence gathering took


# collects the occurrences of six-way combination of class parameters in the
# non-class(nclData) files
def getSixWayResults():
    start_time = time.time()  # starts a timer to time to four-way combinations
    output = ""
    file = open("6Wayresults.csv", "a")
    file.write("occurrences,pct,param1,param2,param3,param4,param5,param6,value1,value2,value3,value4,value5,value6,nrn\n")

    # determines for each combination the number of occurrences in the non-class file
    for i in range(ncn - 5):
        for j in range(i + 1, ncn - 4):
            for k in range(j + 1, ncn - 3):
                for l in range(k + 1, ncn - 2):
                    for m in range(l + 1, ncn - 1):
                        for n in range(m + 1, ncn):
                            for rf in range(1, nrc):
                                in_pass_count = 0
                                for rp in range(1, nrn):
                                    if (xcldata[rf][i] == ncldata[rp][i] and xcldata[rf][j] == ncldata[rp][j] and
                                            xcldata[rf][k] == ncldata[rp][k] and xcldata[rf][l] == ncldata[rp][l] and xcldata[rf][m] == ncldata[rp][m] and xcldata[rf][n] == ncldata[rp][n]):
                                        in_pass_count += 1
                                output = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}\n".format(
                                    in_pass_count,
                                    in_pass_count / (nrn - 1),
                                    xcldata[0][i],
                                    xcldata[0][j],
                                    xcldata[0][k],
                                    xcldata[0][l],
                                    xcldata[0][m],
                                    xcldata[0][n],
                                    xcldata[rf][i],
                                    xcldata[rf][j],
                                    xcldata[rf][k],
                                    xcldata[rf][l],
                                    xcldata[rf][m],
                                    xcldata[rf][n],nrn-1)
                                file.write(output)  # writes the result of the current combination to the output file

    file.close()
    print("6-Way runtime %s" % (time.time() - start_time)) # outputs the time the occurrence gathering took


# clears the UI objects
def ClearUI():
    rptBox2Way['text'] = ""
    rptBox3Way['text'] = ""
    rptBox4Way['text'] = ""
    rptBox5Way['text'] = ""
    rptBox6Way['text'] = ""

    statBox2Way["text"] = ""
    statBox3Way["text"] = ""
    statBox4Way["text"] = ""
    statBox5Way["text"] = ""
    statBox6Way["text"] = ""

    progress2Way['value'] = 0
    progress3Way['value'] = 0
    progress4Way['value'] = 0
    progress5Way['value'] = 0
    progress6Way['value'] = 0


def btnLoadOutput_Click():
    # prompts the user to select a file
    global filenameOutput
    filenameOutput = filedialog.askopenfilename(initialdir="/", title="Select Output File")

    # puts file name in the GUI
    txtOutputInfo.insert(0, filenameOutput)

    # checks that a destination was selected
    if filenameOutput != '':
        runOutputBtn['state'] = ACTIVE


def btnLoadOutputRun_Click():
    global coverageLevel
    #getStatisticsFromOutput(filenameOutput, str(coverageLevel) + "WayAnalysis.txt", str(coverageLevel) + "WayZero.txt", str(coverageLevel) + "WayHundred.txt", coverageLevel)
    #combinationAnalysis(filenameOutput, str(coverageLevel) + "WayCombFreq.txt", filenameClass, coverageLevel)
    createDataFrame(filenameOutput, coverageLevel)


def createDataFrame(fileName, coverage):
    df = pd.DataFrame()
    fileIn = open(fileName, 'r')
    occurencenumbers = []
    occurrencepct = []
    #param1 = []
    #param2 = []
    #val1 = []
    #val2 = []
    count = 0
    highestpossible = 0
    for line in fileIn:
        if count != 0:
            parts = line.split(",")
            occurencenumbers.append(int(parts[0]))
            occurrencepct.append(float(parts[1]))
            #param1.append(parts[2].strip(','))
            #param2.append(parts[3].strip(','))
            #val1.append(parts[4])
            #val2.append(parts[5].strip('\n'))
            if int(coverage) == 2:
                highestpossible = int(parts[6].strip('\n'))
            elif int(coverage) == 3:
                highestpossible = int(parts[8].strip('\n'))
            elif int(coverage) == 4:
                highestpossible = int(parts[10].strip('\n'))
            elif int(coverage) == 5:
                highestpossible = int(parts[12].strip('\n'))
            elif int(coverage) == 6:
                highestpossible = int(parts[14].strip('\n'))
            elif int(coverage) == 1:
                highestpossible = int(parts[4].strip('\n'))
        count += 1

    df['Occurrences'] = occurencenumbers
    df['PCT'] = occurrencepct
    #df['Param1'] = param1
    #df['Param2'] = param2
    #df['Value1'] = val1
    #df['Value2'] = val2

    # creates a histogram with the relative number of frequencies
    histOccurrence = plt.figure(figsize=(7, 3))
    bins_numbers = []
    for i in range(highestpossible+1):
        bins_numbers.append(i)
    n, bins, patches = plt.hist(occurencenumbers, bins=bins_numbers)

    # finds total number of combinations
    total = 0
    for i in n:
        total += i

    # turns the occurrence numbers into proportions
    new_n = []
    for num in n:
        new_n.append(num / total)
    new_n.append(0)

    # create bar chart and display it on screen
    barOccurence = plt.figure(figsize=(7, 3))
    bar(bins_numbers, new_n)
    plt.title('Combination Occurrences')
    plt.xlabel('Occurrences')
    plt.ylabel('Proportion')
    plt.savefig(fileName.strip(".csv") + ".png")

    # create a canvas and display it on the screen
    if int(coverage) == 2:
        canvas1 = FigureCanvasTkAgg(barOccurence, twoWayTab)
        canvas_widget = canvas1.get_tk_widget()
        canvas_widget.grid(row=3, column=0)
    elif int(coverage) == 3:
        canvas1 = FigureCanvasTkAgg(barOccurence, threeWayTab)
        canvas_widget = canvas1.get_tk_widget()
        canvas_widget.grid(row=3, column=0)
    elif int(coverage) == 4:
        canvas1 = FigureCanvasTkAgg(barOccurence, fourWayTab)
        canvas_widget = canvas1.get_tk_widget()
        canvas_widget.grid(row=3, column=0)
    elif int(coverage) == 5:
        canvas1 = FigureCanvasTkAgg(barOccurence, fiveWayTab)
        canvas_widget = canvas1.get_tk_widget()
        canvas_widget.grid(row=3, column=0)
    elif int(coverage) == 6:
        canvas1 = FigureCanvasTkAgg(barOccurence, sixWayTab)
        canvas_widget = canvas1.get_tk_widget()
        canvas_widget.grid(row=3, column=0)
    elif int(coverage) == 1:
        canvas1 = FigureCanvasTkAgg(barOccurence, oneWayTab)
        canvas_widget = canvas1.get_tk_widget()
        canvas_widget.grid(row=3, column=0)

    #fig1, ax1 = plt.subplots()
    #ax1.pie(n[0:5], labels=bins_numbers[0:5])
    #ax1.figure.set_size_inches(3,3)
    #ax1.axis('equal')
    #canvas2 = FigureCanvasTkAgg(fig1, oneWayTab)
    #canvas_widget2 = canvas2.get_tk_widget()
    #canvas_widget2.grid(row=3, column=0)


# takes the output file for a given interaction level and then generates
# statistics about the number of occurrences of class combinations in non-class
# file
def getStatisticsFromOutput(infile, outfile, zeroFile, hundredFile, coverage):
    fileIn = open(infile, 'r')
    fileOut = open(outfile, 'w')
    fileZero = open(zeroFile, 'w')
    fileHundred = open(hundredFile, 'w')

    # combination counts for each category
    zeroCount = 0
    zeroToNine = 0
    tenToNineteen = 0
    twentyToTwentynine = 0
    thirtyToThirtynine = 0
    fourtyToFoutynine = 0
    fiftyToFiftynine = 0
    sixtyToSixtynine = 0
    seventyToSeventynine = 0
    eightyToEightynine = 0
    ninetyToNinetynine = 0

    hundred = 0
    count = 0
    total = 0

    # loops through the contents of the file
    for line in fileIn:
        count += 1
        parts = line.split(",")
        percent = int(parts[0])
        total += percent
        # finds which group the combination occurrence number belongs to
        if 10 > percent >= 0:
            zeroToNine += 1
            if percent == 0:
                zeroCount += 1
                if coverage == 2:
                    fileZero.write(parts[2] + "," + parts[3] + "," + parts[4] + "," + parts[5])
                elif coverage == 3:
                    fileZero.write(parts[2] + "," + parts[3] + "," + parts[4] + "," + parts[5] + parts[6] + "," + parts[7])
                elif coverage == 4:
                    fileZero.write(parts[2] + "," + parts[3] + "," + parts[4] + "," + parts[5] + parts[6] + "," + parts[7] + "," + parts[8] + "," + parts[9])
                elif coverage == 5:
                    fileZero.write(parts[2] + "," + parts[3] + "," + parts[4] + "," + parts[5] + parts[6] + "," + parts[7] + "," + parts[8] + "," + parts[9] + "," + parts[10] + "," + parts[11])
                elif coverage == 6:
                    fileZero.write(parts[2] + "," + parts[3] + "," + parts[4] + "," + parts[5] + parts[6] + "," + parts[7] + "," + parts[8] + "," + parts[9] + "," + parts[10] + "," + parts[11] + "," + parts[12] + "," + parts[13])
        elif 20 > percent >= 10:
            tenToNineteen += 1
        elif 30 > percent >= 20:
            twentyToTwentynine += 1
        elif 40 > percent >= 30:
            thirtyToThirtynine += 1
        elif 50 > percent >= 40:
            fourtyToFoutynine += 1
        elif 60 > percent >= 50:
            fiftyToFiftynine += 1
        elif 70 > percent >= 60:
            sixtyToSixtynine += 1
        elif 80 > percent >= 70:
            seventyToSeventynine += 1
        elif 90 > percent >= 80:
            eightyToEightynine += 1
        elif 100 > percent >= 90:
            ninetyToNinetynine += 1
        elif percent == 100:
            hundred += 1
            if coverage == 2:
                fileHundred.write(parts[2] + "," + parts[3] + "," + parts[4] + "," + parts[5])
            elif coverage == 3:
                fileHundred.write(parts[2] + "," + parts[3] + "," + parts[4] + "," + parts[5] + parts[6] + "," + parts[7])
            elif coverage == 4:
                fileHundred.write(
                    parts[2] + "," + parts[3] + "," + parts[4] + "," + parts[5] + parts[6] + "," + parts[7] + "," +
                    parts[8] + "," + parts[9])
            elif coverage == 5:
                fileHundred.write(
                    parts[2] + "," + parts[3] + "," + parts[4] + "," + parts[5] + parts[6] + "," + parts[7] + "," +
                    parts[8] + "," + parts[9] + "," + parts[10] + "," + parts[11])
            elif coverage == 6:
                fileHundred.write(
                    parts[2] + "," + parts[3] + "," + parts[4] + "," + parts[5] + parts[6] + "," + parts[7] + "," +
                    parts[8] + "," + parts[9] + "," + parts[10] + "," + parts[11] + "," + parts[12] + "," + parts[13])

    # writes the important statistics to the output file
    fileOut.write("Entries analyzed :" + str(count) + '\n')
    fileOut.write("Average occurrence:" + str(total/count) + '\n')
    fileOut.write("Zero Count:" + str(zeroCount) + '\n')
    fileOut.write("Zero Percent:" + str(zeroCount/count) + '\n')
    fileOut.write("0-9 Count:" + str(zeroToNine) + '\n')
    fileOut.write("0-9 Percent:" + str(zeroToNine / count) + '\n')
    fileOut.write("10-19 Count:" + str(tenToNineteen) + '\n')
    fileOut.write("10-19 Percent:" + str(tenToNineteen / count) + '\n')
    fileOut.write("20-29 Count:" + str(twentyToTwentynine) + '\n')
    fileOut.write("20-29 Percent:" + str(twentyToTwentynine / count) + '\n')
    fileOut.write("30-39 Count:" + str(thirtyToThirtynine) + '\n')
    fileOut.write("30-39 Percent:" + str(thirtyToThirtynine / count) + '\n')
    fileOut.write("40-49 Count:" + str(fourtyToFoutynine) + '\n')
    fileOut.write("40-49 Percent:" + str(fourtyToFoutynine / count) + '\n')
    fileOut.write("50-59 Count:" + str(fiftyToFiftynine) + '\n')
    fileOut.write("50-59 Percent:" + str(fiftyToFiftynine / count) + '\n')
    fileOut.write("60-69 Count:" + str(sixtyToSixtynine) + '\n')
    fileOut.write("60-69 Percent:" + str(sixtyToSixtynine / count) + '\n')
    fileOut.write("70-79 Count:" + str(seventyToSeventynine) + '\n')
    fileOut.write("70-79 Percent:" + str(seventyToSeventynine / count) + '\n')
    fileOut.write("80-89 Count:" + str(eightyToEightynine) + '\n')
    fileOut.write("80-89 Percent:" + str(eightyToEightynine / count) + '\n')
    fileOut.write("90-99 Count:" + str(ninetyToNinetynine) + '\n')
    fileOut.write("90-99 Percent:" + str(ninetyToNinetynine / count) + '\n')
    fileOut.write("100 Count:" + str(hundred) + '\n')
    fileOut.write("100 Percent:" + str(hundred / count) + '\n')

    # closes the file
    fileIn.close()
    fileOut.close()
    fileHundred.close()
    fileZero.close()


def combinationAnalysis(infile, outfile, classfile, coverage):
    fileIn = open(infile, 'r')
    fileClass = open(classfile, 'r')
    fileOut = open(outfile, 'w')

    attributes = fileClass.readline().split(',')
    for i in range(0, len(attributes)):
        attributes[i] = attributes[i].strip("\n")

    occurences = {i: 0 for i in attributes}
    numbers = {i: 0 for i in attributes}
    for line in fileIn:
        parts = line.split(",")
        occurenceNum = int(parts[0])
        if coverage == 2:
            for attribute in attributes:
                if attribute in parts[2] or attribute in parts[3]:
                    occurences[attribute] += occurenceNum
                    numbers[attribute] += 1
        elif coverage == 3:
            for attribute in attributes:
                if attribute in parts[2] or attribute in parts[3] or attribute in parts[4]:
                    occurences[attribute] += occurenceNum
                    numbers[attribute] += 1
        elif coverage == 4:
            for attribute in attributes:
                if attribute in parts[2] or attribute in parts[3] or attribute in parts[4] or attribute in parts[5]:
                    occurences[attribute] += occurenceNum
                    numbers[attribute] += 1
        elif coverage == 5:
            for attribute in attributes:
                if attribute in parts[2] or attribute in parts[3] or attribute in parts[4] or attribute in parts[5] or attribute in parts[6]:
                    occurences[attribute] += occurenceNum
                    numbers[attribute] += 1
        elif coverage == 6:
            for attribute in attributes:
                if attribute in parts[2] or attribute in parts[3] or attribute in parts[4] or attribute in parts[5] or attribute in parts[6] or attribute in parts[7]:
                    occurences[attribute] += occurenceNum
                    numbers[attribute] += 1

    fileOut.write("attribute,occurrences,entries,average\n")
    for entry in occurences:
        fileOut.write(str(entry))
        fileOut.write(",")
        fileOut.write(str(occurences[entry]))
        fileOut.write(",")
        fileOut.write(str(numbers[entry]))
        fileOut.write(",")
        fileOut.write(str(occurences[entry]/numbers[entry]))
        fileOut.write("\n")
    print(occurences)
    print(numbers)


def change_dropdown(*args):
    global coverageLevel
    coverageLevel = tkvar.get()


####################################################
# creation of GUI window
# Faultloc
root = Tk()
root.title("Class feature difference analysis")
topFrame = LabelFrame(root, text="File Information")
topFrame.pack()

# tabControl1 stores all the testing tabs
tabControl1 = ttk.Notebook(root, width=750)

# tabPage0 tab for one-way testing
oneWayTab = Frame(tabControl1)
# tabPage1 tab for two-way testing
twoWayTab = Frame(tabControl1)
# tabPage2 tab for three-way testing
threeWayTab = Frame(tabControl1)
# tabPage3 tab for four-way testing
fourWayTab = Frame(tabControl1)
# tabPage4 tab for five-way testing
fiveWayTab = Frame(tabControl1)
# tabPage5 tab for six-way testing
sixWayTab = Frame(tabControl1)

# adds the tabs to the tabControl1 -- the tab group object
tabControl1.add(oneWayTab, text="1-Way")
tabControl1.add(twoWayTab, text="2-Way")
tabControl1.add(threeWayTab, text="3-Way")
tabControl1.add(fourWayTab, text="4-Way")
tabControl1.add(fiveWayTab, text="5-Way")
tabControl1.add(sixWayTab, text="6-Way")
tabControl1.pack()

# variables for the state of the file loading
stateClassFile = False
stateNominalFile = False

# btnLoadFaultFile allows the user to load class file
btnLoadFaultFile = ttk.Button(topFrame, text="Load Class", width=10, command=BtnLoadFaultFile_Click)
btnLoadFaultFile.grid(row=0, column=2)
# txtFaultContents displays the contents of the class file
txtFaultContents = Entry(topFrame, width=50)
txtFaultContents.grid(row=0, column=1)
# btnLoadNominalFile allow the user to load the nominal file
btnLoadFaultFile = ttk.Button(topFrame, text="Load Nominal", width=10, command=nomButton_Click)
btnLoadFaultFile.grid(row=1, column=2)
# txtNominalInfo where the class file name is displayed
txtNominalInfo = Entry(topFrame, width=50)
txtNominalInfo.grid(row=1, column=1)
# txtFaultInfo where the nominal file name is displayed
txtFaultInfo = Scrollbar(topFrame)
txtFaultInfo.grid(row=2, column=1)
faultList = Listbox(topFrame, yscrollcommand=txtFaultInfo.set, width=50) # this is where the data is actually displayed
# btnTest button to start the running of the occurrence analysis
btnTest = ttk.Button(topFrame, text="RUN", width=50, command=btnTest_Click, state=DISABLED)
btnTest.grid(row=3, column=1)

#####################################
# output info
# btnLoadOutput loads the output file to be analyzed
btnLoadOutput = ttk.Button(topFrame, text="Load Output", command=btnLoadOutput_Click)
btnLoadOutput.grid(row=4, column=2)
txtOutputInfo = Entry(topFrame, width=50)
txtOutputInfo.grid(row=4, column=1)
# outputLabel label to indicate where the output file name is displayed
outputLabel = Label(topFrame, text="Output File:", anchor="w", width=20)
outputLabel.grid(row=4, column=0)

# drop down menu
levels = {1,2,3,4,5,6}
tkvar = StringVar(root)
tkvar.set(2) # set the default option
popupMenu = OptionMenu(topFrame, tkvar, *levels)
coverageLabel = Label(topFrame, text="Choose a Coverage")
coverageLabel.grid(row=5, column=0)
popupMenu.grid(row=5, column=1)
# run output analysis
runOutputBtn = ttk.Button(topFrame, text="Run Output Analysis", command=btnLoadOutputRun_Click, state=DISABLED)
runOutputBtn.grid(row=5, column=2)
tkvar.trace('w', change_dropdown)
################################################


# rptBox1Way
rptBox1Way = ttk.Entry(oneWayTab, width=50)
rptBox1Way.grid(row=2, ipadx=200)
# rptBox2way
rptBox2Way = ttk.Entry(twoWayTab, width=50)
rptBox2Way.grid(row=2, ipadx=200)
# rptBox3way
rptBox3Way = ttk.Entry(threeWayTab, width=50)
rptBox3Way.grid(row=2, ipadx=200)
# rptBox4way
rptBox4Way = ttk.Entry(fourWayTab, width=50)
rptBox4Way.grid(row=2, ipadx=200)
# rptBox5Way
rptBox5Way = ttk.Entry(fiveWayTab, width=50)
rptBox5Way.grid(row=2, ipadx=200)
# rptBox6Way
rptBox6Way = ttk.Entry(sixWayTab, width=50)
rptBox6Way.grid(row=2, ipadx=200)

# variables for the state of the checkboxes
var1Way = IntVar()
var2Way = IntVar()
var3Way = IntVar()
var4Way = IntVar()
var5Way = IntVar()
var6Way = IntVar()


# chk1WayTest checkbox to enable one-way testing
chk1WayTest = ttk.Checkbutton(oneWayTab, text="Enabled", variable=var1Way)
chk1WayTest.grid(sticky="w", row=0, column=0)
# chk2WayTest checkbox to enable two-way testing
chk2WayTest = ttk.Checkbutton(twoWayTab, text="Enabled", variable=var2Way)
chk2WayTest.grid(sticky="w", row=0, column=0)
# chk3WayTest checkbox to enable three-way testing
chk3WayTest = ttk.Checkbutton(threeWayTab, text="Enabled", variable=var3Way)
chk3WayTest.grid(sticky="w", row=0, column=0)
# chk4WayTest checkbox to enable four-way testing
chk4WayTest = ttk.Checkbutton(fourWayTab, text="Enabled", variable=var4Way)
chk4WayTest.grid(sticky="w", row=0, column=0)
# chk5WayTest checkbox to enable five-way testing
chk5WayTest = ttk.Checkbutton(fiveWayTab, text="Enabled", variable=var5Way)
chk5WayTest.grid(sticky="w", row=0, column=0)
# chk6WayTest checkbox to enable six-way testing
chk6WayTest = ttk.Checkbutton(sixWayTab, text="Enabled", variable=var6Way)
chk6WayTest.grid(sticky="w", row=0, column=0)

# statBox1way place where the output is displayed for two-way combinations
statBox1Way = tk.Text(oneWayTab, width=100)
statBox1Way.grid(row=3)
# statBox2way place where the output is displayed for two-way combinations
statBox2Way = tk.Text(twoWayTab, width=100)
statBox2Way.grid(row=3)
# statBox3Way place where the output is displayed for three-way combinations
statBox3Way = tk.Text(threeWayTab, width=100)
statBox3Way.grid(row=3)
# statBox4way place where the output is displayed for four-way combinations
statBox4Way = tk.Text(fourWayTab, width=100)
statBox4Way.grid(row=3)
# statBox5Way place where the output is displayed for five-way combinations
statBox5Way = tk.Text(fiveWayTab, width=100)
statBox5Way.grid(row=3)
# statBox6Way place where the output is displayed for six-way combinations
statBox6Way = tk.Text(sixWayTab, width=100)
statBox6Way.grid(row=3)


# progress1way displays the level of progress for analysis of two-way combinations
progress1Way = ttk.Progressbar(oneWayTab, orient=HORIZONTAL, mode='determinate', length=750)
progress1Way.grid(sticky="w", row=1)
# progress2way displays the level of progress for analysis of two-way combinations
progress2Way = ttk.Progressbar(twoWayTab, orient=HORIZONTAL, mode='determinate', length=750)
progress2Way.grid(sticky="w", row=1)
# progress3way displays the level of progress for analysis of three-way combinations
progress3Way = ttk.Progressbar(threeWayTab, orient=HORIZONTAL, mode='determinate', length=750)
progress3Way.grid(sticky="w", row=1)
# progress4way displays the level of progress for analysis of four-way combinations
progress4Way = ttk.Progressbar(fourWayTab, orient=HORIZONTAL, mode='determinate', length=750)
progress4Way.grid(sticky="w", row=1)
# progress5way displays the level of progress for analysis of five-way combinations
progress5Way = ttk.Progressbar(fiveWayTab, orient=HORIZONTAL, mode='determinate', length=750)
progress5Way.grid(sticky="w", row=1)
# progress6way displays the level of progress for analysis of six-way combinations
progress6Way = ttk.Progressbar(sixWayTab, orient=HORIZONTAL, mode='determinate', length=750)
progress6Way.grid(sticky="w", row=1)

# fileContentsLabel -- directs the user to where the class file contents are displayed
fileContentsLabel = Label(topFrame, text="Class File Contents:", anchor="w", width=20)
fileContentsLabel.grid(row=2, column=0)
# nominalLabel label to indicate where the nominal file name is displayed
nominalLabel = Label(topFrame, text="Nominal File:", anchor="w", width=20)
nominalLabel.grid(row=1, column=0)
# classLabel label to indicate where the class file is displayed
classLabel = Label(topFrame, text="Class File:", anchor="w", width=20)
classLabel.grid(row=0, column=0)

root.mainloop()
####################################################

