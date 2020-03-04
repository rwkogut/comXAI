from Tkinter import *
import ttk

root = Tk()
root.title("Class feature difference analysis")

topFrame = LabelFrame(root, text="File Information")
topFrame.pack()

classLabel = Label(topFrame, text="Class File:", anchor="w", width=20)
classLabel.grid(row=0, column=0)

nominalLabel = Label(topFrame, text="Nominal File:", anchor="w", width=20)
nominalLabel.grid(row=1, column=0)

fileContentsLabel = Label(topFrame, text="Class File Contents:", anchor="w", width=20)
fileContentsLabel.grid(row=2, column=0)

loadClassBtn = Button(topFrame, text="Load Class", anchor="w", width=10).grid(row=0, column=2)
loadNominalBtn = Button(topFrame, text="Load Nominal", anchor="w", width=10).grid(row=1, column=2)

classFileEntry = Entry(topFrame, width=50).grid(row=0, column=1)
nominalFileEntry = Entry(topFrame, width=50).grid(row=1, column=1)
fileContentsEntry = Entry(topFrame, width=50).grid(row=2, column=1, ipady=40)

runBtn = Button(topFrame, text="RUN", width=50).grid(row=3, column=1)

parentTab = ttk.Notebook(root, width=750)

twoWayTab = Frame(parentTab)
threeWayTab = Frame(parentTab)
fourWayTab = Frame(parentTab)
fiveWayTab = Frame(parentTab)
sixWayTab = Frame(parentTab)

parentTab.add(twoWayTab, text="2-Way")
parentTab.add(threeWayTab, text="3-Way")
parentTab.add(fourWayTab, text="4-Way")
parentTab.add(fiveWayTab, text="5-Way")
parentTab.add(sixWayTab, text="6-Way")
parentTab.pack()

#enabledFrame = ttk.Frame(twoWayTab)
#btn = Checkbutton(enabledFrame, text="Enabled")

ttk.Checkbutton(twoWayTab, text="Enabled").grid(row=0, column=0, ipadx=420)
ttk.Checkbutton(threeWayTab, text="Enabled").grid(row=0, column=0, ipadx=420)
ttk.Checkbutton(fourWayTab, text="Enabled").grid(row=0, column=0, ipadx=420)
ttk.Checkbutton(fiveWayTab, text="Enabled").grid(row=0, column=0, ipadx=420)
ttk.Checkbutton(sixWayTab, text="Enabled").grid(row=0, column=0, ipadx=420)

#ttk.Entry(twoWayTab).grid(row=0, column=0)
#ttk.Entry(threeWayTab).grid(row=0, column=0)
#ttk.Entry(fourWayTab).grid(row=0, column=0)
#ttk.Entry(fiveWayTab).grid(row=0, column=0)
#ttk.Entry(sixWayTab).grid(row=0, column=0)

ttk.Entry(twoWayTab, width=50).grid(row=1, ipadx=200)
ttk.Entry(threeWayTab, width=50).grid(row=1, ipadx=200)
ttk.Entry(fourWayTab, width=50).grid(row=1, ipadx=200)
ttk.Entry(fiveWayTab, width=50).grid(row=1, ipadx=200)
ttk.Entry(sixWayTab, width=50).grid(row=1, ipadx=200)

ttk.Entry(twoWayTab, width=50).grid(row=2, ipadx=200, ipady=150)
ttk.Entry(threeWayTab, width=50).grid(row=2, ipadx=200, ipady=150)
ttk.Entry(fourWayTab, width=50).grid(row=2, ipadx=200, ipady=150)
ttk.Entry(fiveWayTab, width=50).grid(row=2, ipadx=200, ipady=150)
ttk.Entry(sixWayTab, width=50).grid(row=2, ipadx=200, ipady=150)

root.mainloop()