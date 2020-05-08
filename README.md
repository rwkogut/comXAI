# comXAI
# Overview

This repository contains an application used for the testing of machine learning datasets. More specifically, it compares the combinations of a class data-set to a non-class(nominal) datasets. It outputs information related to the appearnence of certains combinations of inputs found in the class set that are also found in the non-class data set.

# Implemented Features 

* GUI interface using the Python Tkinter library
* Cython Implementation in the branch "cython-branch"
* Numba Implementation in the branch "numba-branch"
* Additional Improvements in the branch "additional-improvements"
* 2,3,4,5,6-way combinatorial testing and output
* 2,3,4-way combinatorial testing coverage graphs 
* Analysis of output combination occurrences in non-class file

# Future features 

* String Hashing

# Directories/Files
Main Source File
* Faultloc/Faultloc.py -- Contains the code file for the program

Datasets/Results
* Faultloc/Animals_with_Attributes -- contains a variety of class and non-class csv files for use in the comXAI tool
* Faultloc/Testing Results.zip -- is a zip file that contains the results from testing

once Testing Results.zip is unzipped (takes about 1.5GB of space)
* Faultloc/Testing Results/Analysis Files/Chimp -- contains 2,3,4,5 and 6-way testing summaries 
* Faultloc/Testing Results/Analysis Files/Dalmatian -- contains 2,3,4,5 and 6-way testing summaries 
* Faultloc/Testing Results/Analysis Files/Grizzly Bear -- contains 2,3,4,5 and 6-way testing summaries 
* Faultloc/Testing Results/Zero Occurrence Files/Chimp -- contains 2,3,4,5 and 6-way zero-occurrence combinations
* Faultloc/Testing Results/Zero Occurrence Files/Dalmatian -- contains 2,3,4,5 and 6-way zero-occurrence combinations
* Faultloc/Testing Results/Zero Occurrence Files/Grizzly Bear -- contains 2,3,4,5 and 6-way zero-occurrence combinations
* Faultloc/Testing Results/Combinations/Occurrences/Chimp -- contains 2,3, and 4-way combinations
* Faultloc/Testing Results/Combinations/Occurrences/Dalmatian -- contains 2,3, and 4-way combinations
* Faultloc/Testing Results/Combinations/Occurrences/Grizzly Bear -- contains 2,3, and 4-way combinations


# Dependencies 
matplotlib -- library needed for the coverage graphs 
* Download instructions at https://matplotlib.org/users/installing.html

# Compilation and running instructions 

The code must be run using a Python 3 compiler. Simply run the program with the Python 3 compiler and a GUI window will appear for use.

* For example, run in the command line "python3 Faultloc.py" and the program should run assuming matplotlib and Python 3 is downloaded.

Once the GUI window has been launched there will be buttons that allow you to input class and nominal (non-class) files. Select the level of coverage and click the run button and the program will run and output the statistics to the output window in the GUI.

