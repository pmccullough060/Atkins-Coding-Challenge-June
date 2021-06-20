import re

########################
#       CLASSES        #
########################

class Row:
    def __init__(self, phase, forceX, forceY, forceZ):
        self.phase = phase
        self.forceX = forceX
        self.forceY = forceY
        self.forceZ = forceZ

class Table:
    def __init__(self, name):
        self.name = name
        self._rows = []

    def addRow(self, row):
        self._rows.append(row)
    
class Results:
    def __init__(self, name):
        self.name = name
        self.tables = []

    def getTables(self):
        return self.tables

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
        result = list(filter(None, result))
        return result
        
    def match(self, line):
        return re.search(self.dataRegex, line)

########################
#      FUNCTIONS       #
########################

#^\s*\S+(?:\s+\S+){7,7}\s*$

########################
#      PROGRAM         #
########################

#Initial chunking:
chunker = Chunker("SEASTATE NO[ ]{2,}[0-9]", "MAXIMUM BASE SHEAR", "WAJAC.LIS")
chunks = chunker.getChunks()

#Getting our required data in Lists:
strProcessor = TextDataExtractor(" ", "^\s*\S+(?:\s+\S+){7,7}\s*$")

result = Results("WAJAC.LIS Seastate Data")

for chunk in chunks:
    strProcessor.processLine(chunk, "hello everyone")


