from __future__ import division
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import csv
import sys
import math
import itertools
import datetime
from datetime import timedelta
from collections import Counter

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from pylab import *

#####################
# load class file into array
filenameClass = ""
xcldata = list()
nrc = 0
ncc = 0
xclass = set()
ctxclass = list()
allclass = set()
######################
# load nominal file into array
filenameNominal = ""
ncldata = list()
nrn = 0
ncn = 0
nonclass = set()
######################
# compute total possible variable-value settings
# count of values for each parameter
nvals = []
ncoms2 = 0
ncoms3 = 0
ncoms4 = 0
totvals1 = 0
totvals2 = 0
totvals3 = 0
totvals4 = 0
######################
# 2-way variables
######################


# action for the BtnLoadFaultFile
def BtnLoadFaultFile_Click():
    global filenameClass
    filenameClass = filedialog.askopenfilename(initialdir="/", title="Select Class File", filetypes=(("csv files","*.csv"),("all files","*.*")))
    txtFaultContents.insert(0, filenameClass)
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

    for j in range(ncc):
        for i in range(nrc):
            xclass[j].add(xcldata[i][j])
            ctxclass[j].append(xcldata[i][j])
            allclass[j].add(xcldata[i][j])


def nomButton_Click():
    global filenameNominal
    filenameNominal = filedialog.askopenfilename(initialdir="/", title="Select Nominal File", filetypes=(("csv files","*.csv"),("all files","*.*")))
    txtNominalInfo.insert(0, filenameNominal)
    stateNominalFile = True

    btnTest['state'] = ACTIVE  # TODO -- add error checking later

    global ncldata
    with open(filenameNominal) as csvfile:
        ncldata = list(csv.reader(csvfile))

    loadNomFile()


def loadNomFile():
    global nrn
    nrn = len(ncldata)
    global ncn
    ncn = len(ncldata[0])
    if ncn != ncc:
        raise IOError("Both files must have same number of parameters")

    global nonclass
    nonclass = [set() for _ in range(ncn)]

    for j in range(ncn):
        for i in range(nrn):
            nonclass[j].add(ncldata[i][j])
            allclass[j].add(ncldata[i][j])


# action for the run button
def btnTest_Click():
    computeValueSettings()
    if var2Way.get() == 1:  # TODO -- FIX LATER
        get2WayResults()
    if var3Way.get() == 1:
        getThreeWayResults()
    if var4Way.get() == 1:
        getFourWayResults()
    if var5Way.get() == 1:
        print("five way test")
    if var6Way.get() == 1:
        print("Six way test")


# Computes the statistics needed for the finding all results
def computeValueSettings():
    global nvals
    nvals = []
    for i in range(ncc):
        vset = (xclass[i].copy()).union(nonclass[i])
        nvals.append(len(vset))

    global ncoms2
    global ncoms3
    global ncoms4
    ncoms2 = int(math.factorial(ncc) / (2 * math.factorial(ncc - 2)))
    ncoms3 = int(math.factorial(ncc) / (6 * math.factorial(ncc - 3)))
    ncoms4 = int(math.factorial(ncc) / (24 * math.factorial(ncc - 4)))

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


# finds the two way results
def get2WayResults():
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

    # output 2way diffs
    tot2waydiffs = 0
    for i in range(ncc - 1):
        for j in range(i + 1, ncc):
            if len(diff2way[i][j]) > 0:
                tot2waydiffs += len(diff2way[i][j])

                pass_count = 0
                for xtup in diff2way[i][j]:
                    output = str(i) + str(j) + xtup[0] + xtup[1] + " = " + str(pass_count/ncc) + "of cases"
                    TwoWayList.insert(END, ' '.join(output))
                    if diff2way[i][j] == xtup:
                        pass_count += 1
    TwoWayList.grid(row=3, column=0, ipadx=200, ipady=150)
    statBox2Way.config(command=TwoWayList.yview)

    rptBox2Way.insert(0, "Combinations = " + str(ncc) + " , Settings = " + str(ncc*ncc))  # TODO -- FIX

    # creates and outputs two way coverage plots
    yvals2 = []
    for i in range(ncc - 1):
        for j in range(i + 1, ncc):
            yvals2.append(len(xclass2w[i][j]) / (nvals[i] * nvals[j]))
    xvals2 = range(ncoms2)
    ## Coverage as in CCM;  completeness

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
    plot = plt.figure(figsize=(3,3))
    plt.figaspect(.5)
    plt.plot(Xd2, Y2, color="red", label="2-way")

    # create a canvas and display it on the screen
    canvas2Way = FigureCanvasTkAgg(plot, twoWayTab)
    canvas_widget = canvas2Way.get_tk_widget()
    canvas_widget.grid(row=3, column=0)


# finds the three way results
def getThreeWayResults():
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

    # output 3way diffs
    tot3waydiffs = 0
    for i in range(ncc - 2):
        for j in range(i + 1, ncc - 1):
            for k in range(j + 1, ncc):
                if len(diff3way[i][j][k]) > 0:
                    tot3waydiffs += len(diff3way[i][j][k])
                    pass_count = 0
                    for xtup in diff3way[i][j][k]:
                        output = str(i) + str(j) + str(k) + xtup[0] + xtup[1] + xtup[2] + " = " + str(pass_count/ncc) + " of cases"
                        ThreeWayList.insert(END, ' '.join(output))
                        if diff3way[i][j] == xtup:
                            pass_count += 1
    ThreeWayList.grid(row=3, ipadx=200, ipady=150)
    statBox3Way.config(command=ThreeWayList.yview)
    rptBox3Way.insert(0,"Combinations = " + str(ncc) + " , Settings = " + str(ncc * ncc * ncc))  # TODO -- FIX

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


# determines the four way results
def getFourWayResults():
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

    # output 4way diffs
    tot4waydiffs = 0
    f4 = open('diff4way.csv', 'w')
    f4.write("i,j,k,m,  ival,jval,kval,mval\n")
    for i in range(ncc - 3):
        for j in range(i + 1, ncc - 2):
            for k in range(j + 1, ncc - 1):
                for m in range(k + 1, ncc):
                    if len(diff4way[i][j][k][m]) > 0:
                        # print("4way ", i,j,k,m)
                        # for tup1 in diff4way[i][j][k][m]:
                        #    print(tup1)
                        tot4waydiffs += len(diff4way[i][j][k][m])
                        pass_count = 0
                        for xtup in diff4way[i][j][k][m]:
                            output = str(i) + str(j) + str(k) + str(m) + xtup[0] + xtup[1] + xtup[2] + xtup[3] + " = " + str(pass_count / ncc) + " of cases"
                            FourWayList.insert(END, ' '.join(output))
                            if diff4way[i][j] == xtup:
                                pass_count += 1

    FourWayList.grid(row=3, ipadx=200, ipady=150)
    statBox4Way.config(command=FourWayList.yview)
    rptBox4Way.insert(0, "Combinations = " + str(ncc) + " , Settings = " + str(ncc * ncc * ncc))  # TODO -- FIX

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


####################################################
# creation of GUI window
# Faultloc
root = Tk()
root.title("Class feature difference analysis")
topFrame = LabelFrame(root, text="File Information")
topFrame.pack()

# tabControl1
tabControl1 = ttk.Notebook(root, width=750)

# tabPage1
twoWayTab = Frame(tabControl1)
# tabPage2
threeWayTab = Frame(tabControl1)
# tabPage3
fourWayTab = Frame(tabControl1)
# tabPage4
fiveWayTab = Frame(tabControl1)
# tabPage5
sixWayTab = Frame(tabControl1)

# adds the tabs to the tabControl1 -- the tab group object
tabControl1.add(twoWayTab, text="2-Way")
tabControl1.add(threeWayTab, text="3-Way")
tabControl1.add(fourWayTab, text="4-Way")
tabControl1.add(fiveWayTab, text="5-Way")
tabControl1.add(sixWayTab, text="6-Way")
tabControl1.pack()

# variables for the state of the file loading
stateClassFile = False
stateNominalFile = False

# btnLoadFaultFile
btnLoadFaultFile = ttk.Button(topFrame, text="Load Class", width=10, command=BtnLoadFaultFile_Click)
btnLoadFaultFile.grid(row=0, column=2)
# txtFaultContents
txtFaultContents = Entry(topFrame, width=50)
txtFaultContents.grid(row=0, column=1)
# btnLoadNominalFile
btnLoadFaultFile = ttk.Button(topFrame, text="Load Nominal", width=10, command=nomButton_Click)
btnLoadFaultFile.grid(row=1, column=2)
# txtNominalInfo
txtNominalInfo = Entry(topFrame, width=50)
txtNominalInfo.grid(row=1, column=1)
# txtFaultInfo
txtFaultInfo = Scrollbar(topFrame)
txtFaultInfo.grid(row=2, column=1)
faultList = Listbox(topFrame, yscrollcommand=txtFaultInfo.set, width=50) #this is where the data is actually displayed
# btnTest
btnTest = ttk.Button(topFrame, text="RUN", width=50, command=btnTest_Click, state=DISABLED)
btnTest.grid(row=3, column=1)

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
var2Way = IntVar()
var3Way = IntVar()
var4Way = IntVar()
var5Way = IntVar()
var6Way = IntVar()

# chk2WayTest
chk2WayTest = ttk.Checkbutton(twoWayTab, text="Enabled", variable=var2Way)
chk2WayTest.grid(sticky="w", row=0, column=0)
# chk3WayTest
chk3WayTest = ttk.Checkbutton(threeWayTab, text="Enabled", variable=var3Way)
chk3WayTest.grid(sticky="w", row=0, column=0)
# chk4WayTest
chk4WayTest = ttk.Checkbutton(fourWayTab, text="Enabled", variable=var4Way)
chk4WayTest.grid(sticky="w", row=0, column=0)
# chk5WayTest
chk5WayTest = ttk.Checkbutton(fiveWayTab, text="Enabled", variable=var5Way)
chk5WayTest.grid(sticky="w", row=0, column=0)
# chk6WayTest
chk6WayTest = ttk.Checkbutton(sixWayTab, text="Enabled", variable=var6Way)
chk6WayTest.grid(sticky="w", row=0, column=0)

# statBox2way
statBox2Way = Scrollbar(twoWayTab)
statBox2Way.grid(row=3)
TwoWayList = Listbox(twoWayTab, yscrollcommand=statBox2Way.set, width=50)  # this is where the data is actually displayed

# statBox3Way
statBox3Way = Scrollbar(threeWayTab)
statBox3Way.grid(row=3)
ThreeWayList = Listbox(threeWayTab, yscrollcommand=statBox3Way.set, width=50)  # this is where the data is actually displayed

# statBox4way
statBox4Way = Scrollbar(fourWayTab)
statBox4Way.grid(row=3)
FourWayList = Listbox(fourWayTab, yscrollcommand=statBox4Way.set, width=50) # this is where the data is actually displayed
# statBox5Way
statBox5Way = Scrollbar(fiveWayTab)
statBox5Way.grid(row=3)
FiveWayList = Listbox(fiveWayTab, yscrollcommand=statBox5Way.set, width=50)
# statBox6Way
statBox6Way = Scrollbar(sixWayTab)
statBox6Way.grid(row=3)
SixWayList = Listbox(sixWayTab, yscrollcommand=statBox6Way.set, width=50)

# progress2way
progress2Way = ttk.Progressbar(twoWayTab, orient=HORIZONTAL, mode='determinate', length=750)
progress2Way.grid(sticky="w", row=1)
# progress3way
progress3Way = ttk.Progressbar(threeWayTab, orient=HORIZONTAL, mode='determinate', length=750)
progress3Way.grid(sticky="w", row=1)
# progress4way
progress4Way = ttk.Progressbar(fourWayTab, orient=HORIZONTAL, mode='determinate', length=750)
progress4Way.grid(sticky="w", row=1)
# progress5way
progress5Way = ttk.Progressbar(fiveWayTab, orient=HORIZONTAL, mode='determinate', length=750)
progress5Way.grid(sticky="w", row=1)
# progress6way
progress6Way = ttk.Progressbar(sixWayTab, orient=HORIZONTAL, mode='determinate', length=750)
progress6Way.grid(sticky="w", row=1)

# fileContentsLabel formerly label3
fileContentsLabel = Label(topFrame, text="Class File Contents:", anchor="w", width=20)
fileContentsLabel.grid(row=2, column=0)
# nominalLabel formerly label2
nominalLabel = Label(topFrame, text="Nominal File:", anchor="w", width=20)
nominalLabel.grid(row=1, column=0)
# classLabel formerly label1
classLabel = Label(topFrame, text="Class File:", anchor="w", width=20)
classLabel.grid(row=0, column=0)

root.mainloop()
####################################################


