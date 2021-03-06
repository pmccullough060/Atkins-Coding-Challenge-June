import re
import time
import pandas as pd
import matplotlib.pyplot as plt

########################
#         ABOUT        #
########################

# Atkins coding challenge June 2021
# This script parses the attached text file, plots the selected sea state table and outputs *ALL* of the seastate table data to an excel file.
# Instead of loading the file into memory it reads in line by line
# The Chunker class uses regex expressions to extract the "chunks" of the file that are of interest
# The chunks are iterated over using the DataExtractor which finds and formats the useful data
# The DataExtractor is useful as sometimes there are line breaks etc within the useful data that should be ignored

########################
#         SETUP        #
########################

# run the following commands from the directory containing main.py:
# py -m venv venv
# .\venv\Scripts\activate
# py --version | pip --version  (check its all working)
# Either:
# pip install pandas
# pip install matplotlib
# pip install openpyxl
# Or:
# pip install -r requirements.txt
# pip list (check everything is installed in the venv)

########################
#       CLASSES        #
########################

class Table:
    def __init__(self, name):
        self.name = name
        self.rows = {}
    
    def addRow(self, data):
        self.rows["step " + str(data[0])] = [data[1], data[2], data[3], data[4]]

    def getDict(self):
        return self.rows

class Results:
    def __init__(self, name):
        self.name = name
        self.tables = []

    def getTables(self):
        return self.tables

    def getTable(self, index):
        return self.tables[index]

    def addTable(self, table):
        self.tables.append(table)

class Chunker:
    def __init__(self, startRegex, finishRegex, fileName):
        self.startRegex = startRegex
        self.finishRegex = finishRegex
        self.fileName = fileName
        self.chunks = []

    def processFile(self):
        babyChunk = ""
        chunkin = False

        with open(self.fileName) as file:
            for line in file:
                if(chunkin):
                    if(self.finish(line)):
                        self.chunks.append(babyChunk)
                        babyChunk = ""
                        chunkin = False
                    else:
                        babyChunk += line
                else:
                    if(self.start(line)):
                        chunkin = True
                        babyChunk += line

    def finish(self, line):
        return re.search(self.finishRegex, line)

    def start(self, line):
        return re.search(self.startRegex, line) 

    def getChunks(self):
        return self.chunks

class DataExtractor:
    def __init__(self, splitToken, dataRegex):
        self.splitToken = splitToken
        self.dataRegex = dataRegex

    def processLine(self, line):
        result = []
        if(self.match(line)):
                result = line.split(self.splitToken)
        return list(filter(None, result))
        
    def match(self, line):
        return re.search(self.dataRegex, line)

########################
#      FUNCTIONS       #
########################

#Function go here if needed in future.

########################
#      PROGRAM         #
########################

#start timer
t0 = time.time()

#Initial chunking:
chunker = Chunker("SEASTATE NO[ ]{2,}[0-9]", "MAXIMUM BASE SHEAR", "WAJAC.LIS")
chunker.processFile()
chunks = chunker.getChunks()

#Getting our required table data in Lists from a line of input data
#*if* it matches the regex:
dataExtTableData = DataExtractor(" ", "^\s*[0-9]+(?:\s+\S+){7,7}\s*$")

result = Results("Seastate Data")

for count in range(0, len(chunks)):
    
    table = Table("Table " + str(count+1))
    result.addTable(table)

    for line in chunks[count].splitlines():
        lineResult = dataExtTableData.processLine(line)
        if lineResult:
            lineResult = [float(item) for item in lineResult]
            table.addRow(lineResult)

#Creating the pandas dataframes:
dfs = []
for table in result.getTables():
    data = table.getDict()
    df = pd.DataFrame.from_dict(data, 
                                orient="index", 
                                columns=["PHASE", "Fx", "Fy", "Fz"])
    dfs.append(df)

#outputting dataframes to excel:
with pd.ExcelWriter("output.xlsx") as writer:
    for count in range(0, len(dfs)):
        dfs[count].to_excel(writer, sheet_name="SEASTATE NO " + str(count+1))

#Time taken
t1 = time.time()
total = t1 - t0

#Script Info
print("##### Job Completed #####")
print(len(dfs), "Tables processed")
print("Time Taken: {:f} seconds".format(total))

#Plot the first table dataframe
plot = dfs[0].plot(x="PHASE", title="Fx, Fy, Fz Against Phase Angle")
plot.set_xlim(0,360)
plot.set_xlabel("Phase Angle (Deg)")
plot.set_ylabel("Force (N)")

plt.show()
