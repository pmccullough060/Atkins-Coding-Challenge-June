import re
import pandas as pd
import matplotlib.pyplot as plt

########################
#         ABOUT        #
########################

#Atkins coding challenge June 2021
#This script parses the attached text file, plots the selected table and outputs *ALL* of the seastate table data to an excel file.

########################
#         SETUP        #
########################

# run the following commands from the directory containing main.py:
# py -m venv venv
# .\venv\Scripts\activate
# py --version | pip --version  (check its all working)
# pip install pandas
# pip install matplotlib
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

    def updateName(self, name):
        self.name = name

    def getDict(self):
        return self.rows

class Results:
    def __init__(self, name):
        self.name = name
        self.tables = []

    def getTables(self):
        return self.tables

    def addTable(self, table):
        self.tables.append(table)

    def getTable(self, index):
        return self.tables[index]

class Chunker:
    def __init__(self, startRegexExp, terminateRegexExp, fileName):
        self.startRegexExp = startRegexExp
        self.terminateRegexExp = terminateRegexExp
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
        return re.search(self.terminateRegexExp, line)

    def start(self, line):
        return re.search(self.startRegexExp, line) 

    def getChunks(self):
        return self.chunks

class TextDataExtractor:
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

#If functions required in future add here:

########################
#      PROGRAM         #
########################

#Initial chunking:
chunker = Chunker("SEASTATE NO[ ]{2,}[0-9]", "MAXIMUM BASE SHEAR", "WAJAC.LIS")
chunker.processFile()
chunks = chunker.getChunks()

#Getting our required data in Lists from a line of input data *if* it matches the regex:
strProcessor = TextDataExtractor(" ", "^\s*[0-9]+(?:\s+\S+){7,7}\s*$")

result = Results("WAJAC.LIS Seastate Data")

#populating the results object:
for chunk in chunks:
    table = Table(chunk[1])
    result.addTable(table)

    for line in chunk.splitlines():
        lineResult = strProcessor.processLine(line)
        if lineResult:
            lineResult = [float(item) for item in lineResult]
            table.addRow(lineResult)

#Fetch seastate No.1 Table
selectedTable = result.getTable(1)

#Creating the pandas dataframes:
df = pd.DataFrame.from_dict(selectedTable.getDict(), 
                            orient='index', 
                            columns=['PHASE', 'Fx', 'Fy', 'Fz'])

#Plot from the dataframe
df.plot()
plt.show()

#outputting to excel:


print("complete")

